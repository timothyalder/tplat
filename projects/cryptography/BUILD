# load("@rules_python//python:defs.bzl", "py_library")
load("@rules_python//python:packaging.bzl", "py_wheel")
load("@aspect_rules_py//py:defs.bzl", "py_library")

# Defining a python library. We will package this library as a wheel
py_library(
    name = "poker", 
    deps = [
        "@py3_deps//pandas:pkg",
        "@py3_deps//scipy:pkg",
        "@py3_deps//pytest:pkg",
    ], 
    srcs = [
        "poker/__init__.py",
        "poker/main.py",
    ], 
    imports = ["."],
    visibility = ["//visibility:public"],
)

# Package some specific py_library targets, without their dependencies
py_wheel(
    name = "poker_whl",
    # Package data. We're building "poker-1.0.0-py3-none-any.whl"
    distribution = "poker",
    python_tag = "py3",
    version = "1.0.0",
    deps = [
        ":poker",
    ],
    strip_path_prefixes = ["projects/poker",],
)
    