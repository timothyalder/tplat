load("//rules:doc.bzl", "doc_publish", "doc_menu_item")

doc_menu_item(
    name = "GitHub",
    url ="https://github.com/timothyalder/tplat",
    weight=1000,
)

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
    menu = [
        ":GitHub",
    ],
    title = "tplat",
    visibility = ["//visibility:public"],
)
