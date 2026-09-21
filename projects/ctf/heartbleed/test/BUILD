load("@rules_shell//shell:sh_test.bzl", "sh_test")

sh_test(
    name = "heartbleed_sources_test",
    srcs = ["heartbleed_sources_test.sh"],
    data = [
        "//projects/ctf/heartbleed:build_nginx_layer.sh",
        "//projects/ctf/heartbleed:nginx.conf",
        "//projects/ctf/heartbleed:heartbleed_flag_module/config",
        "//projects/ctf/heartbleed:heartbleed_flag_module/ngx_http_heartbleed_flag_module.c",
    ],
)
