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

- `idor_image`: OCI image containing the challenge service.
- Application: dependency-free Python web service listening on port `8080`.
- Data store: resettable seeded data containing normal-user and administrator
  notes.
- Smoke test: confirms the service starts and the intended authorization flaw
  remains present.

## Safety and lifecycle

Run the challenge only on an isolated local container network. Use synthetic
flags and credentials, do not publish the exposed port, and recreate the
container and seeded data for every reset.

## Running the challenge

Load the image into the configured local container runtime:

```sh
bazel run //projects/ctf/idor:load_idor_image
```

Then run it with a loopback-only port binding and a disposable data volume:

```sh
docker run --rm --name idor-ctf -p 127.0.0.1:8080:8080 idor-ctf:latest
```

Open `http://127.0.0.1:8080` and solve the challenge through the running
service. Stop the container to reset its state.

## Next steps

1. Build and load `//projects/ctf/idor:idor_image` in a local container runtime.
2. Start it on an isolated local network and interact with it at port `8080`.
3. Solve the challenge without reading the application source.
