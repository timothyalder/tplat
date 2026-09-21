# Heartbleed CTF

## Purpose and safety

This is a deliberately vulnerable, local-only exercise for
[CVE-2014-0160 (Heartbleed)](https://nvd.nist.gov/vuln/detail/CVE-2014-0160).
It runs nginx compiled with OpenSSL 1.0.1f, the affected OpenSSL release. The
OCI image is based directly on `nginxinc/nginx-unprivileged:trixie`, the same
base used by the IDOR CTF. Its normal nginx executable cannot use OpenSSL 1.0.1f
(it is ABI-linked to patched `libssl.so.3`), so a Bazel action adds an nginx
executable with the vulnerable library statically compiled in.

Never deploy, publish, or reuse this image. It intentionally exposes a
memory-disclosure vulnerability. Use a synthetic flag only, bind its port to
loopback, and remove the container after the exercise.

## What is in the image

- A Bazel `genrule` compiles nginx with OpenSSL 1.0.1f and
  `--with-openssl-opt=no-shared`, then creates the layer consumed by
  `oci_image`. That statically embeds the old TLS library rather than linking
  the patched library in the nginx base.
- nginx listens on unprivileged TLS port `8443` and offers only a harmless
  `/healthz` route. The flag is not in a route or a response.
- The bundled nginx module copies a synthetic flag into OpenSSL-owned worker
  memory at startup. Repetition makes a local CTF observation practical while
  retaining the Heartbleed-style memory disclosure as the intended path.

## Build/load and run

Build and load the `oci_image` into the configured local container runtime:

```sh
bazel run //projects/ctf/heartbleed:load_heartbleed_image
```

The first build downloads the versioned source archives and compiles the layer, so
it requires network access and a Linux/amd64 C build environment. No Dockerfile
or `docker build` is used.

Run the challenge with a loopback-only binding:

```sh
docker run --rm --name heartbleed-ctf -p 127.0.0.1:8443:8443 heartbleed-ctf:latest
```

In another terminal, confirm the ordinary TLS service works. The self-signed
certificate is expected, hence `-k`:

```sh
curl -k https://127.0.0.1:8443/healthz
```

Stop it with `docker stop heartbleed-ctf` (or Ctrl-C in the terminal that is
running it). `--rm` removes the container when it stops.

## Challenge hints

Heartbleed is a bounds-check failure in the TLS heartbeat request handler. A
heartbeat request contains a one-byte type, a two-byte declared payload length,
then the actual payload and padding. Vulnerable OpenSSL versions allocate a
response using the declared length and copy that many bytes without first
checking that the received record really contained that many bytes. The extra
bytes are process memory.

1. First perform a standard TLS handshake and inspect the ServerHello
   extensions. An affected peer advertises the TLS heartbeat extension
   (extension type `0x000f`). A generic TLS scanner may identify the old
   OpenSSL version, but extension inspection is the reliable indicator here.
2. After the handshake, send a TLS record with content type `24`
   (`heartbeat`). Its heartbeat message type is `1` (request). Keep the actual
   payload very short, but declare a much larger payload length, such as
   `0x4000`. TLS records after the handshake must be protected with the
   negotiated cipher state, so a raw plaintext TCP write is not sufficient.
3. Decrypt the peer's heartbeat response and look for message type `2`
   (response). Save each response and search the concatenated bytes for the
   `flag{` prefix. Heap layout is variable; repeat requests and reconnect a few
   times if needed. Do not send records larger than TLS permits.

At the wire level, the vulnerable part of a request is conceptually:

```text
type = 0x01 | claimed_payload_length = 0x4000 | actual_payload = 0x41 | padding
```

The critical mistake to recognize when implementing a detector or a lab PoC is
the mismatch between the **claimed** payload length and the bytes actually
present. A correct implementation rejects that mismatch before copying any
payload. Keep any PoC limited to `127.0.0.1:8443` (or another system you own
and have explicitly designated for this exercise).

## Verification and reset

Confirm the built service really contains the intentionally old library rather
than the base image's current one:

```sh
docker run --rm --entrypoint /usr/local/sbin/nginx-heartbleed heartbleed-ctf:latest -V
```

The configure arguments should include `--with-openssl=.../openssl-1.0.1f`.
After the exercise, remove the local image as well:

```sh
docker image rm heartbleed-ctf:latest
```
