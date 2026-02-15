
def _doc_serve_impl(ctx):
    serve_script = ctx.actions.declare_file(ctx.label.name + ".sh")

    site_name = ctx.attr.site_target_name
    script_content = """#!/usr/bin/env bash
set -euo pipefail

# Locate Bazel runfiles dir
RUNFILES_DIR="${RUNFILES_DIR:-$(dirname $0)/../..}"

# Compute the output dir for the site
SITE_OUTPUT="${RUNFILES_DIR}/projects/docs/{site}.output"

echo "Serving Jekyll from ${SITE_OUTPUT}"
cd "${SITE_OUTPUT}"
bundle exec jekyll serve
""".format(site = site_name)

    ctx.actions.write(
        output = serve_script,
        content = script_content,
        is_executable = True,
    )

    return DefaultInfo(
        executable = serve_script,
        runfiles = ctx.runfiles(files = [serve_script]),
    )


doc_site_serve = rule(
    implementation = _doc_serve_impl,
    executable = True,
)