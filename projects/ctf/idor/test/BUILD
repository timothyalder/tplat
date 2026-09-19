load("@pypi//:requirements.bzl", "requirement")
load("@rules_python//python:defs.bzl", "py_test")

py_test(
    name = "idor_test",
    main = "test.py",
    srcs = ["test.py"],
    deps = [
        "//projects/ctf/idor:server",
        requirement("pytest"),
    ],
)