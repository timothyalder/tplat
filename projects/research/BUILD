load("//rules:doc.bzl", "doc_section")

doc_section(
    name = "research",
    srcs = [
        "thesis.md",
        "vcsel.md",
        "bushfire.md",
    ],
    data = [":data"],
    index = "index.md",
    slug = "research",
    visibility = ["//visibility:public"],
)

filegroup(
    name = "data",
    srcs = glob(["*.pdf"]),
    visibility = [
        "//projects/docs:__subpackages__",
    ],
)
