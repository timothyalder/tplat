load("@pypi//:requirements.bzl", "requirement")
load("@rules_python//python:defs.bzl", "py_library")

# Defining a python library. We will package this library as a wheel
py_library(
    name = "qr",
    srcs = [
        "main.py",
    ],
    imports = ["."],
    visibility = ["//visibility:public"],
    deps = [
        requirement("qrcode"),
    ],
)
