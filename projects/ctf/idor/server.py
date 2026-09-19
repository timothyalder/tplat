import hashlib
import json
import os
import secrets
import sqlite3
from http import HTTPStatus
from http.cookies import SimpleCookie
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path


FLAG = "flag{object_level_authorization_is_required}"


class ChallengeStore:
    def __init__(self, database_path):
        self.database_path = database_path
        self.sessions = {}
        self.initialize()

    def connect(self):
        connection = sqlite3.connect(self.database_path)
        connection.row_factory = sqlite3.Row
        return connection

    def initialize(self):
        with self.connect() as connection:
            connection.executescript(
                """
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY,
                    username TEXT NOT NULL UNIQUE,
                    password_hash TEXT NOT NULL
                );
                CREATE TABLE IF NOT EXISTS notes (
                    id INTEGER PRIMARY KEY,
                    owner_id INTEGER NOT NULL,
                    title TEXT NOT NULL,
                    body TEXT NOT NULL,
                    FOREIGN KEY(owner_id) REFERENCES users(id)
                );
                """
            )
            connection.execute(
                "INSERT OR IGNORE INTO users (id, username, password_hash) VALUES (?, ?, ?)",
                (1, "administrator", password_hash("not-for-login")),
            )
            connection.execute(
                """
                INSERT OR IGNORE INTO notes (id, owner_id, title, body)
                VALUES (?, ?, ?, ?)
                """,
                (1, 1, "Administrator note", FLAG),
            )

    def register(self, username, password):
        with self.connect() as connection:
            cursor = connection.execute(
                "INSERT INTO users (username, password_hash) VALUES (?, ?)",
                (username, password_hash(password)),
            )
            user_id = cursor.lastrowid
            connection.execute(
                "INSERT INTO notes (owner_id, title, body) VALUES (?, ?, ?)",
                (user_id, "Welcome", "This is your private note."),
            )
        return user_id

    def authenticate(self, username, password):
        with self.connect() as connection:
            user = connection.execute(
                "SELECT id, password_hash FROM users WHERE username = ?",
                (username,),
            ).fetchone()
        if user is None or user["password_hash"] != password_hash(password):
            return None
        return user["id"]

    def create_session(self, user_id):
        token = secrets.token_urlsafe(32)
        self.sessions[token] = user_id
        return token

    def user_for_session(self, token):
        return self.sessions.get(token)

    def notes_for_user(self, user_id):
        with self.connect() as connection:
            notes = connection.execute(
                "SELECT id, title, body FROM notes WHERE owner_id = ? ORDER BY id",
                (user_id,),
            ).fetchall()
        return [dict(note) for note in notes]

    def note_by_id(self, note_id):
        with self.connect() as connection:
            note = connection.execute(
                "SELECT id, owner_id, title, body FROM notes WHERE id = ?",
                (note_id,),
            ).fetchone()
        return None if note is None else dict(note)


def password_hash(password):
    return hashlib.sha256(password.encode("utf-8")).hexdigest()


class ChallengeHandler(BaseHTTPRequestHandler):
    server_version = "IDOR-CTF/1.0"

    def do_GET(self):
        if self.path == "/":
            self.send_html(HTTPStatus.OK, page())
            return
        if self.path == "/healthz":
            self.send_json(HTTPStatus.OK, {"status": "ok"})
            return
        if self.path == "/api/notes":
            user_id = self.require_user()
            if user_id is not None:
                self.send_json(HTTPStatus.OK, {"notes": self.server.store.notes_for_user(user_id)})
            return
        if self.path.startswith("/api/notes/"):
            user_id = self.require_user()
            if user_id is None:
                return
            note_id = self.note_id()
            if note_id is None:
                return
            note = self.server.store.note_by_id(note_id)
            if note is None:
                self.send_json(HTTPStatus.NOT_FOUND, {"error": "note not found"})
                return
            self.send_json(HTTPStatus.OK, {"note": note})
            return
        self.send_json(HTTPStatus.NOT_FOUND, {"error": "not found"})

    def do_POST(self):
        if self.path not in {"/api/register", "/api/login"}:
            self.send_json(HTTPStatus.NOT_FOUND, {"error": "not found"})
            return
        payload = self.request_json()
        if not isinstance(payload, dict):
            self.send_json(HTTPStatus.BAD_REQUEST, {"error": "invalid JSON"})
            return
        username = payload.get("username")
        password = payload.get("password")
        if not valid_credentials(username, password):
            self.send_json(HTTPStatus.BAD_REQUEST, {"error": "invalid username or password"})
            return
        if self.path == "/api/register":
            try:
                user_id = self.server.store.register(username, password)
            except sqlite3.IntegrityError:
                self.send_json(HTTPStatus.CONFLICT, {"error": "username already exists"})
                return
        else:
            user_id = self.server.store.authenticate(username, password)
            if user_id is None:
                self.send_json(HTTPStatus.UNAUTHORIZED, {"error": "invalid credentials"})
                return
        session = self.server.store.create_session(user_id)
        self.send_json(
            HTTPStatus.CREATED if self.path.endswith("register") else HTTPStatus.OK,
            {"user_id": user_id},
            headers={"Set-Cookie": f"session={session}; HttpOnly; SameSite=Lax; Path=/"},
        )

    def request_json(self):
        try:
            content_length = int(self.headers.get("Content-Length", "0"))
            if content_length > 4096:
                raise ValueError
            return json.loads(self.rfile.read(content_length))
        except (ValueError, json.JSONDecodeError):
            return None

    def require_user(self):
        cookie = SimpleCookie(self.headers.get("Cookie"))
        session = cookie.get("session")
        user_id = self.server.store.user_for_session(session.value) if session else None
        if user_id is None:
            self.send_json(HTTPStatus.UNAUTHORIZED, {"error": "login required"})
        return user_id

    def note_id(self):
        try:
            return int(self.path.rsplit("/", 1)[1])
        except ValueError:
            self.send_json(HTTPStatus.BAD_REQUEST, {"error": "invalid note identifier"})
            return None

    def send_json(self, status, payload, headers=None):
        body = json.dumps(payload).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        for name, value in (headers or {}).items():
            self.send_header(name, value)
        self.end_headers()
        self.wfile.write(body)

    def send_html(self, status, content):
        body = content.encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, format, *args):
        return


def valid_credentials(username, password):
    return (
        isinstance(username, str)
        and isinstance(password, str)
        and 3 <= len(username) <= 32
        and 8 <= len(password) <= 128
    )


def page():
    return """<!doctype html>
<html lang="en">
<head><meta charset="utf-8"><title>IDOR CTF</title></head>
<body>
<h1>Private Notes</h1>
<p>Register or log in to view your notes.</p>
<form id="register"><h2>Register</h2><input name="username" placeholder="username" required><input name="password" type="password" placeholder="password" required><button>Register</button></form>
<form id="login"><h2>Log in</h2><input name="username" placeholder="username" required><input name="password" type="password" placeholder="password" required><button>Log in</button></form>
<button id="notes">My notes</button><pre id="result"></pre>
<script>
const result = document.querySelector('#result');
for (const form of document.querySelectorAll('form')) form.addEventListener('submit', async event => {
  event.preventDefault();
  const response = await fetch('/api/' + form.id, {method: 'POST', headers: {'Content-Type': 'application/json'}, body: JSON.stringify(Object.fromEntries(new FormData(form)))});
  result.textContent = await response.text();
});
document.querySelector('#notes').addEventListener('click', async () => {
  const response = await fetch('/api/notes');
  result.textContent = await response.text();
});
</script>
</body></html>"""


def main():
    data_directory = Path(os.environ.get("IDOR_DATA_DIR", "/tmp/idor"))
    data_directory.mkdir(parents=True, exist_ok=True)
    server = ThreadingHTTPServer(("0.0.0.0", 8080), ChallengeHandler)
    server.store = ChallengeStore(data_directory / "idor.db")
    server.serve_forever()


if __name__ == "__main__":
    main()
