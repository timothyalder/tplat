load("@rules_cc//cc:cc_toolchain_config_lib.bzl", "tool_path")
load("@rules_cc//cc/common:cc_common.bzl", "cc_common")
load("@rules_cc//cc/toolchains:cc_toolchain_config_info.bzl",
     "CcToolchainConfigInfo")

def _impl(ctx):
    return cc_common.create_cc_toolchain_config_info(
        ctx = ctx,

        toolchain_identifier = "windows_x86_64",
        host_system_name = "windows",
        target_system_name = "windows",
        target_cpu = "x86_64",
        target_libc = "msvcrt",
        compiler = "clang-cl",
        abi_version = "msvc",
        abi_libc_version = "msvcrt",

        tool_paths = [
            tool_path(name = "gcc", path = "C:/Program Files/LLVM/bin/clang-cl.exe"),
            tool_path(name = "ld",  path = "C:/Program Files/LLVM/bin/clang-cl.exe"),
            tool_path(name = "ar", path = "C:/Program Files/LLVM/bin/llvm-lib.exe"),
            tool_path(name = "nm", path = "C:/Program Files/LLVM/bin/llvm-nm.exe"),
            tool_path(name = "objdump", path = "C:/Program Files/LLVM/bin/llvm-objdump.exe"),
            tool_path(name = "strip", path = "C:/Program Files/LLVM/bin/llvm-strip.exe"),
            tool_path(name = "cpp", path = "NUL"),
            tool_path(name = "gcov", path = "NUL"),
        ],

        cxx_builtin_include_directories = [
            "C:/Program Files/LLVM/lib/clang/17/include",
            "C:/Program Files/Microsoft Visual Studio/2022/BuildTools/VC/Tools/MSVC/include",
            "C:/Program Files (x86)/Windows Kits/10/Include",
        ],
    )

cc_toolchain_config = rule(
    implementation = _impl,
    provides = [CcToolchainConfigInfo],
)
