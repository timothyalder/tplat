# load("@rules_python//python:defs.bzl", "py_library")
load("@rules_python//python:packaging.bzl", "py_wheel")
load("@aspect_rules_py//py:defs.bzl", "py_library")

# Defining a python library. We will package this library as a wheel
py_library(
    name = "cryptography", 
    deps = [
        "@py3_deps//tqdm:pkg",
        "@py3_deps//sympy:pkg",
        "@py3_deps//pytest:pkg",
    ], 
    srcs = glob(["cryptography/**/*.py"])
    imports = ["."],
    visibility = ["//visibility:public"],
)

# Package some specific py_library targets, without their dependencies
py_wheel(
    name = "cryptography_whl",
    # Package data. We're building "cryptography-1.0.0-py3-none-any.whl"
    distribution = "cryptography",
    python_tag = "py3",
    version = "1.0.0",
    deps = [
        ":cryptography",
    ],
    strip_path_prefixes = ["projects/cryptography",],
)
    