load("@npm//:markdownlint-cli/package_json.bzl", markdownlint = "bin")
load("@aspect_rules_js//js:defs.bzl", "js_library")

markdownlint.markdownlint_binary(
    name = "markdownlint_cli",
    visibility = ["//visibility:public"],
)

js_library(
    name = "style_json",
    srcs = ["style.json"],
    visibility = ["//visibility:public"],
)
