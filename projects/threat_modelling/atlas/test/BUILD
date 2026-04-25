load("@pypi//:requirements.bzl", "requirement")
load("@rules_python//python:defs.bzl", "py_test")

py_test(
    name = "test",
    main = "test_atlas.py",
    srcs = [
        "test_atlas.py",
    ],
    data = [
        "//projects/threat_modelling/atlas/data",
    ],
    deps = [
        "//projects/threat_modelling/atlas",
        requirement("pytest"),
    ],
)
