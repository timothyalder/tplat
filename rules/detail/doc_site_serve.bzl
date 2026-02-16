load(":_doc_providers.bzl", "DocSiteInfo")

def _doc_serve_impl(ctx):
    site_output = ctx.attr.site[DocSiteInfo].output_dir
    script = ctx.actions.declare_file(ctx.label.name + ".sh")

    script_content = """#!/usr/bin/env bash
set -euo pipefail
pwd
echo "Serving Jekyll from {site}"
cd "{site}"
bundle
bundle exec jekyll serve
""".format(site = site_output.short_path)

    # Set an environment variable to pass output dir?

    ctx.actions.write(
        output = script,
        content = script_content,
        is_executable = True,
    )

    return DefaultInfo(
        executable = script,
        runfiles = ctx.runfiles(files = [script, site_output]),
    )


doc_site_serve = rule(
    implementation = _doc_serve_impl,
    attrs = {
        "site": attr.label(
            providers = [DocSiteInfo],
            mandatory = True,
        ),
    },
    executable = True,
)