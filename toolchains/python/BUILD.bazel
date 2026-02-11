load("@rules_multirun//:defs.bzl", "multirun")
load("@rules_uv//uv:pip.bzl", "pip_compile")
load("@rules_uv//uv:venv.bzl", "create_venv", "sync_venv")

pip_compile(
    name = "generate_requirements_linux",
    data = ["requirements3.in"],
    py3_runtime = "@python_3_12//:py3_runtime",
    python_platform = "x86_64-unknown-linux-gnu",
    requirements_in = "requirements3_linux.in",
    requirements_txt = "requirements3_linux.txt",
)

pip_compile(
    name = "generate_requirements_windows",
    data = ["requirements3.in"],
    py3_runtime = "@python_3_12//:py3_runtime",
    python_platform = "x86_64-pc-windows-msvc",
    requirements_in = "requirements3_windows.in",
    requirements_txt = "requirements3_windows.txt",
)

pip_compile(
    name = "generate_requirements_darwin",
    data = ["requirements3.in"],
    py3_runtime = "@python_3_12//:py3_runtime",
    python_platform = "x86_64-apple-darwin",
    requirements_in = "requirements3_darwin.in",
    requirements_txt = "requirements3_darwin.txt",
)

multirun(
    name = "generate_requirements",
    commands = [
        ":generate_requirements_linux",
        ":generate_requirements_darwin",
        ":generate_requirements_windows",
    ],
    # Running in a single threaded mode allows consecutive `uv` invocations to benefit
    # from the `uv` cache from the first run.
    jobs = 1,
)

# create_venv(name = "create-venv")

# sync_venv(
#     name = "sync-venv-darwin",
#     destination_folder = ".sync-venv"
#     requirements_txt = "requirements3_darwin.txt",
# )
