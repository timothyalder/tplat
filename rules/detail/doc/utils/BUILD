load("@rules_python//python:defs.bzl", "py_binary", "py_library", "py_test")

py_library(
    name = "formatter_lib",
    srcs = ["formatter.py"],
    imports = ["."],
)

py_binary(
    name = "formatter",
    srcs = ["formatter.py"],
    visibility = ["//visibility:public"],
)

py_test(
    name = "formatter_test",
    size = "small",
    srcs = ["formatter_test.py"],
    main = "formatter_test.py",
    deps = [":formatter_lib"],
)
