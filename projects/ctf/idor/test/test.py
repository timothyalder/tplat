import http.client
import json
import tempfile
import threading
import unittest

from server import ChallengeHandler, ChallengeStore
from http.server import ThreadingHTTPServer


class IdorChallengeTest(unittest.TestCase):
    def setUp(self):
        self.temporary_directory = tempfile.TemporaryDirectory()
        self.server = ThreadingHTTPServer(("127.0.0.1", 0), ChallengeHandler)
        self.server.store = ChallengeStore(f"{self.temporary_directory.name}/idor.db")
        self.thread = threading.Thread(target=self.server.serve_forever)
        self.thread.start()

    def tearDown(self):
        self.server.shutdown()
        self.thread.join()
        self.server.server_close()
        self.temporary_directory.cleanup()

    def request(self, method, path, body=None, headers=None):
        connection = http.client.HTTPConnection("127.0.0.1", self.server.server_port)
        connection.request(method, path, body=body, headers=headers or {})
        response = connection.getresponse()
        payload = response.read()
        result = response.status, dict(response.getheaders()), json.loads(payload)
        connection.close()
        return result

    def test_authenticated_user_can_access_another_users_note(self):
        status, headers, _ = self.request(
            "POST",
            "/api/register",
            body=json.dumps({"username": "participant", "password": "correct-horse"}),
            headers={"Content-Type": "application/json"},
        )
        self.assertEqual(status, 201)
        session = headers["Set-Cookie"].split(";", 1)[0]

        status, _, payload = self.request(
            "GET",
            "/api/notes/1",
            headers={"Cookie": session},
        )

        self.assertEqual(status, 200)
        self.assertTrue(payload["note"]["body"].startswith("flag{"))
