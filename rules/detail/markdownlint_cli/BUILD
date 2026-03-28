load("@aspect_rules_js//js:defs.bzl", "js_binary")

exports_files([
    "style.json",
])

js_binary(
    name = "markdownlint_cli",
    data = ["//:node_modules/markdownlint-cli"],
    entry_point = "markdownlint_cli.mjs",
    # entry_point = "node_modules/markdownlint-cli/markdownlint.js",
    visibility = ["//visibility:public"],
)
