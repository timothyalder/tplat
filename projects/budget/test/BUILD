load("@pypi//:requirements.bzl", "requirement")
load("@rules_python//python:defs.bzl", "py_test")

py_test(
    name = "test",
    srcs = [
        "test.py",
    ],
    data = [
        "//projects/budget/test/data",
    ],
    deps = [
        "//projects/budget",
        requirement("pytest"),
    ],
)
