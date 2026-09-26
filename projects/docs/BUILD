load("//rules:doc.bzl", "doc_publish", "doc_menu_item")

doc_menu_item(
    name = "GitHub",
    url = "https://github.com/timothyalder/tplat",
    weight=1000,
)

doc_menu_item(
    name = "Resume",
    url = "/resume.pdf",
    weight = 2000,
    data = [
        "//projects/docs/data",
    ],
)

doc_publish(
    name = "docs",
    srcs = [
        "//projects/threat_modelling/docs",
        "//projects/fpga/docs",
        "//projects/cryptography/docs",
        "//projects/networking/docs",
        "//projects/linux",
        "//projects/cs",
        "//projects/math/docs",
        "//projects/research"
    ],
    index = "//:README.md",
    menu = [
        ":GitHub",
        ":Resume",
    ],
    title = "tplat",
    visibility = ["//visibility:public"],
)
