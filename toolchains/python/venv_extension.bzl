# toolchains/python/venv_extension.bzl

def _venv_impl(module_ctx):
    # Ensure the requirements file exists in the main repo.
    # Label(...) is available in the module extension execution context.
    module_ctx.read(Label("//toolchains/python:requirements3_darwin.txt"))

    # Create the external repo using the repository rule implemented in rules_uv.
    # NOTE: do NOT call sync_venv(...) directly here — use module_ctx.create_repo.
    module_ctx.create_repo(
        name = "sync_venv_darwin",
        bzl_file = "@rules_uv//uv:venv.bzl",
        rule = "sync_venv",
        kwargs = {
            "requirements_txt": "//toolchains/python:requirements3_darwin.txt",
        },
    )

# export the module extension
venv = module_extension(implementation = _venv_impl)
