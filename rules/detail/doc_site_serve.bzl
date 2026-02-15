def _doc_serve_impl(ctx):
    script = ctx.actions.declare_file(ctx.label.name + ".sh")

    script_content = """#!/usr/bin/env bash
set -euo pipefail

# Locate Bazel runfiles dir
RUNFILES_DIR="${{PWD}}"

# Compute the output dir for the site
SITE_OUTPUT="${{RUNFILES_DIR}}/projects/docs/{site}.output"

echo "Serving Jekyll from ${{SITE_OUTPUT}}"
cd "${{SITE_OUTPUT}}"
bundle exec jekyll serve
""".format(site = ctx.attr.site_dir)

    # Set an environment variable to pass output dir?

    ctx.actions.write(
        output = script,
        content = script_content,
        is_executable = True,
    )

    return DefaultInfo(
        executable = script,
        runfiles = ctx.runfiles(files = [script]),
    )


doc_site_serve = rule(
    implementation = _doc_serve_impl,
    attrs = {
        "site_dir": attr.string(mandatory = True),
    },
    executable = True,
)