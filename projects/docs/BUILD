load("//rules:doc.bzl", "doc_publish")

doc_publish(
    name = "docs",
    srcs = [
        "test.md",
        "//projects/fpga/docs",
        "//projects/translate/docs",
    ],
    index = "index.md",
    title = "tplat",
    visibility = ["//visibility:public"],
)
