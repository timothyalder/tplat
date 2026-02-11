load("@rules_python//python:defs.bzl", "py_test")

py_test(
    name = "test",
    srcs = [
        "test.py",
    ],
    data = [
        "data",
    ],
    deps = [
        "//projects/translate",
    ] + select({
        "@platforms//os:macos": ["@sync_venv_darwin//pytest"],
        "@platforms//os:linux": ["@sync_venv_linux//pytest"],
        "@platforms//os:windows": ["@sync_venv_windows//pytest"],
        "//conditions:default": [],
    }),
)
