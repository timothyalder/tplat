load("@build_bazel_rules_apple//apple:ios.bzl", "ios_application")
load("@build_bazel_rules_apple//apple:macos.bzl", "macos_application")
load("@rules_cc//cc:defs.bzl", "objc_library")
load("@rules_rust//rust:defs.bzl", "rust_static_library")

rust_static_library(
    name = "rust_lib",
    srcs = ["demo.rs"],
    edition = "2018",
    tags = ["manual"],
)

objc_library(
    name = "main_lib",
    srcs = ["main_lib.m"],
    deps = [":rust_lib"],
)

ios_application(
    name = "ios_app",
    bundle_id = "com.example.iosapp",
    families = ["iphone"],
    infoplists = ["Info.plist"],
    minimum_os_version = "13.0",
    deps = [":main_lib"],
)

macos_application(
    name = "macos_app",
    bundle_id = "com.example.macosapp",
    infoplists = ["Info.plist"],
    minimum_os_version = "10.15",
    deps = [":main_lib"],
)
