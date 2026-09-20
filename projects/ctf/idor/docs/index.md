# IDOR CTF plan

## Objective

Build a small web challenge that demonstrates insecure direct object reference
(IDOR), also known as broken object-level authorization (BOLA). A logged-in
participant should be able to access a note owned by another user because the
application validates authentication but not ownership.

## Challenge design

The service will provide user registration and login plus an endpoint for
reading notes by identifier. Seeded users will own separate notes, with the
administrator's note containing a synthetic CTF flag. The vulnerable endpoint
will check that a requester is logged in but intentionally omit the ownership
check.

## Components

- `idor_image`: OCI image based on `nginxinc/nginx-unprivileged`.
- HTTPS server: nginx listens on port `8443` with a self-signed certificate
  generated while the image layer is built.
- Content: a participant can create a fixed session and is only shown note 2;
  note 1 is an administrator-owned HTML document containing the synthetic flag.
- Intended flaw: nginx checks for a session but intentionally does not check
  that `/api/notes/<id>` belongs to that participant.

## Safety and lifecycle

Run the challenge only on an isolated local container network. Use synthetic
flags and credentials, do not publish the exposed port, and recreate the
container and seeded data for every reset.

## Running the challenge

Load the image into the configured local container runtime:

```sh
bazel run //projects/ctf/idor:load_idor_image
```

Then run it with a loopback-only port binding:

```sh
podman run --rm --name idor-ctf -p 127.0.0.1:8443:8443 idor-ctf:latest
```

Open `https://127.0.0.1:8443` and accept the self-signed certificate warning
(or use `curl -k`). The TLS private key is held by nginx; a client never needs
it to establish HTTPS. Stop the container to reset its state.

## Next steps

1. Build and load `//projects/ctf/idor:idor_image` in a local container runtime.
2. Start it on an isolated local network and interact with it over HTTPS at port `8443`.
3. Register, then request `/api/notes/1` using the resulting session to observe
   the intentional IDOR.
