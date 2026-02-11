load("@rules_cc//cc/toolchains:cc_toolchain.bzl", "cc_toolchain")
load(":toolchain_config.bzl", "cc_toolchain_config")

package(default_visibility = ["//visibility:public"])

cc_toolchain_config(
    name = "config",
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
    toolchain_config = ":config",
)

filegroup(name = "empty")
