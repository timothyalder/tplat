load("@rules_cc//cc:cc_toolchain_config_lib.bzl", "tool_path")
load("@rules_cc//cc/common:cc_common.bzl", "cc_common")
load(
    "@rules_cc//cc/toolchains:cc_toolchain_config_info.bzl",
    "CcToolchainConfigInfo",
)

def _impl(ctx):
    return cc_common.create_cc_toolchain_config_info(
        ctx = ctx,
        toolchain_identifier = "linux_x86_64",
        host_system_name = "linux",
        target_system_name = "linux",
        target_cpu = "x86_64",
        target_libc = "glibc",
        compiler = "clang",
        abi_version = "gnu",
        abi_libc_version = "unknown",
        tool_paths = [
            tool_path(name = "gcc", path = "/usr/bin/clang++"),
            tool_path(name = "ld", path = "/usr/bin/clang++"),
            tool_path(name = "ar", path = "/usr/bin/ar"),
            tool_path(name = "cpp", path = "/bin/false"),
            tool_path(name = "nm", path = "/usr/bin/nm"),
            tool_path(name = "strip", path = "/usr/bin/strip"),
            tool_path(name = "objdump", path = "/bin/false"),
        ],
        cxx_builtin_include_directories = [
            "/usr/include/c++",
            "/usr/include",
            "/usr/lib/clang",
        ],
    )

cc_toolchain_config = rule(
    implementation = _impl,
    provides = [CcToolchainConfigInfo],
)
