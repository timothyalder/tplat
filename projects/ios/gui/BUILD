load("@build_bazel_rules_apple//apple:macos.bzl", "macos_application")
load("@build_bazel_rules_swift//swift:swift.bzl", "swift_library")
load("@rules_rust//rust:defs.bzl", "rust_static_library")

rust_static_library(
    name = "rust_lib",
    srcs = ["demo.rs"],
    edition = "2024",
)

# Objective-C wrapper for the Rust library
objc_library(
    name = "rust_bridge",
    hdrs = ["RustBridge.h"],
    deps = [":rust_lib"],
)

swift_library(
    name = "swift_lib",
    srcs = ["ContentView.swift"],
    copts = [
        "-import-objc-header",
        "$(location RustBridge.h)",
    ],
    # swiftc_inputs is the correct attribute to expose the header to $(location)
    swiftc_inputs = ["RustBridge.h"],
    deps = [":rust_bridge"],
)

macos_application(
    name = "macos_app",
    bundle_id = "com.example.macosapp",
    infoplists = ["Info.plist"],
    minimum_os_version = "12.0",
    deps = [":swift_lib"],
)