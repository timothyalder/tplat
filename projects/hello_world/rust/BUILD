load("@rules_rust//rust:defs.bzl", "rust_library", "rust_binary", "rust_test")

rust_library(
    name = "rust_lib",
    srcs = ["lib.rs"],
    deps = [
        "@crates//:anyhow",
    ],
)

rust_binary(
    name = "rust_bin",
    srcs = ["main.rs"],
    deps = [
        ":rust_lib",
        "@crates//:anyhow",
    ],
)

rust_test(
    name = "rust_test",
    crate = ":rust_lib",
)
