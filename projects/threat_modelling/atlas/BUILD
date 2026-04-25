load("@rules_python//python:defs.bzl", "py_binary", "py_library")

py_library(
    name = "atlas",
    srcs = [
        "atlas/__init__.py",
        "atlas/engine.py",
        "atlas/lint.py",
        "atlas/loader.py",
        "atlas/metrics.py",
        "atlas/predicate.py",
        "atlas/report.py",
        "atlas/schema.py",
        "atlas/invariants.py",
    ],
    imports = ["."],
    visibility = ["//visibility:public"],
)

py_binary(
    name = "atlas_cli",
    srcs = [
        "atlas/cli.py",
    ],
    main = "atlas/cli.py",
    data = [
        "//projects/threat_modelling/atlas/data",
    ],
    deps = [
        ":atlas",
    ],
)
