load("@aspect_rules_js//js:defs.bzl", "js_library", "js_binary", "js_test")

js_library(
    name = "js_lib",
    srcs = ["main.js"],
)

js_binary(
    name = "js_bin",
    entry_point = "main.js",
    data = [":js_lib"],
)

js_test(
    name = "js_test",
    entry_point = "test.js",
    data = [":js_lib"],
)