load("@rules_python//python:defs.bzl", "py_library", "py_binary", "py_test")
load("@pypi//:requirements.bzl", "requirement")

py_library(
    name = "python_lib",
    srcs = [
        "main.py"
    ],
    imports = ["."],
    visibility = ["//visibility:public"],
)

py_binary(
    name = "python_bin",
    srcs = [
        "main.py",
    ],
    main = "main.py",
)

py_test(
    name = "python_test",
    main = "test.py",
    srcs = [
        "test.py",
    ],
    deps = [
        ":python_lib",
        requirement("pytest"),
    ]
)