load("//rules:doc.bzl", "doc_publish")

doc_publish(
    name = "docs",
    srcs = [
        "//projects/threat_modelling/docs",
        "//projects/fpga/docs",
        "//projects/cryptography/docs",
        "//projects/linux",
        "//projects/math/docs",
    ],
    index = "index.md",
    title = "tplat",
    visibility = ["//visibility:public"],
)
