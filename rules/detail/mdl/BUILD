load("@rules_ruby//ruby:defs.bzl", "rb_binary")

exports_files([
    "style.rb",
])

rb_binary(
    name = "mdl",
    main = "@bundle//bin:mdl",
    deps = [
        "@bundle",
    ],
    visibility = ["//visibility:public"],
)