load("@rules_rust//rust:defs.bzl", "rust_library", "rust_binary", "rust_test")

rust_library(
    name = "rust_lib",
    srcs = ["src/lib.rs"],
)

rust_binary(
    name = "rust",
    srcs = ["src/main.rs"],
    deps = [":rust_lib"],
)

rust_test(
    name = "rust_test",
    crate = ":rust_lib",
)