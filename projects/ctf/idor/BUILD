load("@rules_oci//oci:defs.bzl", "oci_image", "oci_load")

exports_files(
    [
        "nginx.conf",
        "html/administrator-note.html",
    ],
    visibility = ["//projects/ctf/idor/test:__pkg__"],
)

genrule(
    name = "nginx_layer",
    srcs = [
        "html/administrator-note.html",
        "html/index.html",
        "nginx.conf",
    ],
    outs = ["nginx_layer.tar"],
    cmd = """
        temp_dir=$$(mktemp -d)
        trap 'rm -rf "$$temp_dir"' EXIT
        mkdir -p "$$temp_dir/etc/nginx/conf.d" "$$temp_dir/etc/nginx/tls" "$$temp_dir/usr/share/nginx/html/protected"
        cp "$(location nginx.conf)" "$$temp_dir/etc/nginx/conf.d/default.conf"
        cp "$(location html/index.html)" "$$temp_dir/usr/share/nginx/html/index.html"
        cp "$(location html/administrator-note.html)" "$$temp_dir/usr/share/nginx/html/protected/administrator-note.html"
        openssl req -x509 -newkey rsa:2048 -sha256 -nodes -days 7 \
          -subj '/CN=idor-ctf.local' \
          -keyout "$$temp_dir/etc/nginx/tls/server.key" \
          -out "$$temp_dir/etc/nginx/tls/server.crt" >/dev/null 2>&1
        chmod 0644 "$$temp_dir/etc/nginx/tls/server.key"
        tar -C "$$temp_dir" -cf "$@" etc usr
    """,
)

oci_image(
    name = "idor_image",
    base = "@distroless_nginx",
    cmd = ["nginx", "-g", "daemon off;"],
    exposed_ports = ["8443"],
    tars = [":nginx_layer"],
    labels = {
        "org.opencontainers.image.title": "IDOR CTF",
    },
    visibility = ["//visibility:public"],
)

oci_load(
    name = "load_idor_image",
    image = ":idor_image",
    repo_tags = ["idor-ctf:latest"],
)
