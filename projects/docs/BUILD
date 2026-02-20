load("//rules:doc.bzl", "doc_publish")

doc_publish(
    name = "docs",
    index = "index.md",
    srcs = [
        "//projects/translate/docs",
        "//projects/fpga/docs",
        "test.md",
    ],
    title = "tplat",
    visibility = ["//visibility:public"],
)
