#!/usr/bin/env bash
set -euo pipefail

root="$TEST_SRCDIR/$TEST_WORKSPACE/projects/ctf/heartbleed"

# The layer build compiles the nginx executable with the specific OpenSSL
# release affected by CVE-2014-0160; the OCI target supplies the nginx base.
grep -Fq 'openssl-1.0.1f' "$root/build_nginx_layer.sh"
grep -Fq -- '--with-openssl-opt=no-shared' "$root/build_nginx_layer.sh"

grep -Fq 'listen 8443 ssl;' "$root/nginx.conf"
grep -Fq 'heartbleed_flag_seed on;' "$root/nginx.conf"
grep -Fq 'flag{heartbeats_must_validate_their_length}' \
    "$root/heartbleed_flag_module/ngx_http_heartbleed_flag_module.c"
