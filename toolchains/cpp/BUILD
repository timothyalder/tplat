package(default_visibility = ["//visibility:public"])

toolchain(
    name = "darwin_x86_64_toolchain",
    target_compatible_with = [
        "@platforms//os:macos",
        "@platforms//cpu:x86_64",
    ],
    toolchain = "//toolchains/cpp/darwin:cpp_toolchain",
    toolchain_type = "@bazel_tools//tools/cpp:toolchain_type",
)

toolchain(
    name = "linux_x86_64_toolchain",
    target_compatible_with = [
        "@platforms//os:linux",
        "@platforms//cpu:x86_64",
    ],
    toolchain = "//toolchains/cpp/linux:cpp_toolchain",
    toolchain_type = "@bazel_tools//tools/cpp:toolchain_type",
)

toolchain(
    name = "windows_x86_64_toolchain",
    target_compatible_with = [
        "@platforms//os:windows",
        "@platforms//cpu:x86_64",
    ],
    toolchain = "//toolchains/cpp/windows:cpp_toolchain",
    toolchain_type = "@bazel_tools//tools/cpp:toolchain_type",
)
