load("@rules_python//python:defs.bzl", "py_test")
load("@pypi//:requirements.bzl", "requirement")

py_test(
    name = "test",
    srcs = [
        "test.py",
    ],
    deps = [
        "//projects/cryptography",
        requirement("pytest"),
    ],
)