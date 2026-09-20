load("@rules_shell//shell:sh_test.bzl", "sh_test")

sh_test(
    name = "nginx_test",
    srcs = ["nginx_test.sh"],
    data = [
        "//projects/ctf/idor:nginx.conf",
        "//projects/ctf/idor:html/administrator-note.html",
    ],
)
