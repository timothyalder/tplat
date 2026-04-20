load("@rules_python//python:defs.bzl", "py_library", "py_binary", "py_test")
load("@pypi//:requirements.bzl", "requirement")

py_library(
    name = "main",
    srcs = [
        "main.py"
    ],
    imports = ["."],
    visibility = ["//visibility:public"],
)

py_binary(
    name = "python",
    srcs = [
        "main.py",
    ],
    main = "main.py",
)

py_test(
    name = "test",
    srcs = [
        "test.py",
    ],
    deps = [
        ":main",
        requirement("pytest"),
    ]
)