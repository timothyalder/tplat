load("@rules_oci//oci:defs.bzl", "oci_image", "oci_load")
load("@rules_python//python:defs.bzl", "py_library")

genrule(
    name = "app_layer",
    srcs = ["server.py"],
    outs = ["app_layer.tar"],
    cmd = """
        temp_dir=$$(mktemp -d)
        trap 'rm -rf "$$temp_dir"' EXIT
        mkdir -p "$$temp_dir/app"
        cp "$(location server.py)" "$$temp_dir/app/server.py"
        tar -C "$$temp_dir" -cf "$@" app
    """,
)

oci_image(
    name = "idor_image",
    base = "@distroless_python",
    cmd = ["/app/server.py"],
    exposed_ports = ["8080"],
    tars = [":app_layer"],
    env = {
        "IDOR_DATA_DIR": "/data",
    },
    labels = {
        "org.opencontainers.image.title": "IDOR CTF",
    },
    visibility = ["//visibility:public"],
    volumes = ["/data"],
)

oci_load(
    name = "load_idor_image",
    image = ":idor_image",
    repo_tags = ["idor-ctf:latest"],
)

py_library(
    name = "server",
    srcs = ["server.py"],
    imports = ["."],
    visibility = ["//visibility:private"],
)
