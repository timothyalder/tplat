load("@rules_ruby//ruby:defs.bzl", "rb_library", "rb_binary", "rb_test")

rb_library(
    name = "ruby_lib",
    srcs = ["lib.rb"],
)

rb_binary(
    name = "ruby_bin",
    srcs = ["main.rb"],
    deps = [":ruby_lib"],
)

rb_test(
    name = "ruby_test",
    srcs = ["test.rb"],
    deps = [":ruby_lib"],
)