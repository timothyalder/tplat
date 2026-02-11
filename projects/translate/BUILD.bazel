load("@rules_python//python:defs.bzl", "py_library")
load("@rules_python//python:packaging.bzl", "py_wheel")

# Defining a python library. We will package this library as a wheel
py_library(
    name = "translate",
    srcs = [
        "translate/__init__.py",
        "translate/main.py",
    ],
    imports = ["."],
    visibility = ["//visibility:public"],
    deps = [
        "@sync_venv_darwin//deep_translator",
        "@sync_venv_darwin//tqdm",
    ],
)

# Package some specific py_library targets, without their dependencies
py_wheel(
    name = "translate_whl",
    # Package data. We're building "translate-1.0.0-py3-none-any.whl"
    distribution = "translate",
    python_tag = "py3",
    strip_path_prefixes = ["projects/translate"],
    version = "1.0.0",
    deps = [
        ":translate",
    ],
)
