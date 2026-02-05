load("@rules_cc//cc/toolchains:cc_toolchain.bzl", "cc_toolchain")
load(":toolchain_config.bzl", "cc_toolchain_config")

package(default_visibility = ["//visibility:public"])

cc_toolchain_config(
    name = "toolchain_semantics",
)

cc_toolchain(
    name = "cpp_toolchain",
    all_files = ":empty",
    ar_files = ":empty",
    compiler_files = ":empty",
    dwp_files = ":empty",
    linker_files = ":empty",
    objcopy_files = ":empty",
    strip_files = ":empty",
    toolchain_config = ":toolchain_semantics",
)

filegroup(
    name = "empty",
)

toolchain(
    name = "platform_based_toolchain",
    target_compatible_with = ["@platforms//cpu:x86_64"],
    toolchain = ":cpp_toolchain",
    toolchain_type = "@bazel_tools//tools/cpp:toolchain_type",
)

platform(
    name = "x86_platform",
    constraint_values = ["@platforms//cpu:x86_64"],
)