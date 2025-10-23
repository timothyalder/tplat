load(":doc_site_build.bzl", "doc_site_build")

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


_doc_serve = rule(
    implementation = _doc_serve_impl,
    attrs = {
        "site_target_name": attr.string(mandatory = True),
    },
    executable = True,
)


def doc_publish(name, config = [], skip_validation = False, **kwargs):
    site_target_name = name + "_site"

    # Build the static site first
    doc_site_build(
        name = site_target_name,
        config = config,
        skip_validation = skip_validation,
        **kwargs
    )

    # Define a separate `bazel run` target for serving
    _doc_serve(
        name = site_target_name + "_serve",
        site_target_name = site_target_name,
        visibility = ["//visibility:public"],
    )
