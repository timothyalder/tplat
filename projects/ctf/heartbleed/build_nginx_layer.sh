#!/usr/bin/env bash
set -euo pipefail
output="$1"; nginx_archive="$2"; openssl_archive="$3"; nginx_conf="$4"
index_html="$5"; healthz="$6"; module_config="$7"; module_source="$8"
work_dir="$(mktemp -d)"; trap 'rm -rf "$work_dir"' EXIT
tar -xzf "$nginx_archive" -C "$work_dir"
tar -xzf "$openssl_archive" -C "$work_dir"
mkdir -p "$work_dir/heartbleed_flag_module"
cp "$module_config" "$work_dir/heartbleed_flag_module/config"
cp "$module_source" "$work_dir/heartbleed_flag_module/ngx_http_heartbleed_flag_module.c"
pushd "$work_dir/nginx-1.4.7" >/dev/null
# OpenSSL, not nginx, contains CVE-2014-0160. This nginx release is only used
# for source compatibility with OpenSSL 1.0.1f. The library is built in, so the
# patched libssl supplied by the base image is never loaded.
./configure --prefix=/usr/local/nginx --sbin-path=/usr/local/sbin/nginx-heartbleed \
  --conf-path=/etc/nginx/nginx.conf --pid-path=/tmp/nginx.pid \
  --error-log-path=/dev/stderr --http-log-path=/dev/stdout \
  --without-http_rewrite_module --without-http_gzip_module --with-http_ssl_module \
  --with-openssl="$work_dir/openssl-1.0.1f" --with-openssl-opt=no-shared \
  --add-module="$work_dir/heartbleed_flag_module"
make -j"$(getconf _NPROCESSORS_ONLN 2>/dev/null || echo 1)"
popd >/dev/null
stage="$work_dir/stage"
mkdir -p "$stage/etc/nginx/tls" "$stage/usr/local/sbin" "$stage/usr/share/nginx/html"
cp "$work_dir/nginx-1.4.7/objs/nginx" "$stage/usr/local/sbin/nginx-heartbleed"
cp "$nginx_conf" "$stage/etc/nginx/nginx.conf"
cp "$index_html" "$stage/usr/share/nginx/html/index.html"
cp "$healthz" "$stage/usr/share/nginx/html/healthz"
openssl req -x509 -newkey rsa:2048 -sha256 -nodes -days 7 \
  -subj '/CN=heartbleed-ctf.local' -keyout "$stage/etc/nginx/tls/server.key" \
  -out "$stage/etc/nginx/tls/server.crt" >/dev/null 2>&1
chmod 0644 "$stage/etc/nginx/tls/server.key"
tar -C "$stage" -cf "$output" etc usr
