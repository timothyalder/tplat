load("@rules_oci//oci:defs.bzl", "oci_image", "oci_load")
load("@rules_shell//shell:sh_binary.bzl", "sh_binary")

exports_files(
    [
        "build_nginx_layer.sh",
        "nginx.conf",
        "html/index.html",
        "html/healthz",
        "heartbleed_flag_module/config",
        "heartbleed_flag_module/ngx_http_heartbleed_flag_module.c",
    ],
    visibility = ["//visibility:public"],
)

genrule(
    name = "nginx_layer",
    srcs = [
        "html/index.html",
        "html/healthz",
        "nginx.conf",
        "heartbleed_flag_module/config",
        "heartbleed_flag_module/ngx_http_heartbleed_flag_module.c",
        "@heartbleed_nginx_source//file",
        "@heartbleed_openssl_source//file",
    ],
    tools = [":build_nginx_layer"],
    outs = ["nginx_layer.tar"],
    cmd = "$(location :build_nginx_layer) $@ $(location @heartbleed_nginx_source//file) $(location @heartbleed_openssl_source//file) $(location nginx.conf) $(location html/index.html) $(location html/healthz) $(location heartbleed_flag_module/config) $(location heartbleed_flag_module/ngx_http_heartbleed_flag_module.c)",
)

sh_binary(
    name = "build_nginx_layer",
    srcs = ["build_nginx_layer.sh"],
)

oci_image(
    name = "heartbleed_image",
    base = "@distroless_nginx",
    cmd = ["/usr/local/sbin/nginx-heartbleed", "-g", "daemon off;"],
    exposed_ports = ["8443"],
    labels = {"org.opencontainers.image.title": "Heartbleed CTF"},
    tars = [":nginx_layer"],
    visibility = ["//visibility:public"],
)

oci_load(
    name = "load_heartbleed_image",
    image = ":heartbleed_image",
    repo_tags = ["heartbleed-ctf:latest"],
)
