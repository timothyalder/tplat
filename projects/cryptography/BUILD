load("@rules_python//python:defs.bzl", "py_library")
load("@rules_python//python:packaging.bzl", "py_wheel")
load("@pypi//:requirements.bzl", "requirement")

py_library(
    name = "cryptography", 
    deps = [
        requirement("tqdm"),
        requirement("sympy"),
        requirement("matplotlib"),
    ], 
    srcs = glob(["cryptography/**/*.py"]),
    imports = ["."],
    visibility = ["//visibility:public"],
)

py_wheel(
    name = "cryptography_whl",
    distribution = "cryptography",
    python_tag = "py3",
    version = "1.0.0",
    deps = [
        ":cryptography",
    ],
    strip_path_prefixes = ["projects/cryptography",],
)
    