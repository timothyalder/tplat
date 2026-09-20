#!/usr/bin/env bash
set -euo pipefail

config="$TEST_SRCDIR/$TEST_WORKSPACE/projects/ctf/idor/nginx.conf"
note="$TEST_SRCDIR/$TEST_WORKSPACE/projects/ctf/idor/html/administrator-note.html"

# The container must be nginx-only and expose TLS on the unprivileged port.
grep -Fq 'listen 8443 ssl;' "$config"
grep -Fq 'ssl_certificate_key /etc/nginx/tls/server.key;' "$config"

# The intended vulnerable route only verifies that a participant is logged in;
# it must not require ownership of note 1.
grep -Fq 'location = /api/notes/1 {' "$config"
grep -Fq 'session=participant' "$config"
grep -Fq 'administrator-note.html' "$config"
grep -Fq 'flag{object_level_authorization_is_required}' "$note"
