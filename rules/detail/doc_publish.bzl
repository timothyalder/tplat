load(":doc_site_build.bzl", "doc_site_build")

def doc_publish(name, config = [], skip_validation = False, **kwargs):
    site_target_name = name + "_site"

    # Build the site artefacts first
    doc_site_build(
        name = site_target_name,
        config = config,
        skip_validation = skip_validation,
        **kwargs
    )

    # Generate the content of the serve script
    script_content = ["#!/usr/bin/env bash"]
    script_content.append("""
set -euo pipefail
# Locate the Bazel runfiles directory
RUNFILES_DIR="$${{RUNFILES_DIR:-$$(dirname $$0)/../..}}"
# Compute the output directory of the site target
SITE_OUTPUT="$${{RUNFILES_DIR}}/projects/docs/{site}.output"
echo "Serving Jekyll from $${{SITE_OUTPUT}}"
cd "$${{SITE_OUTPUT}}"
bundle exec jekyll serve
""".format(site=site_target_name))

    # Use genrule to write it as a file
    native.genrule(
        name = name + "_serve_gen",
        outs = [name + "_serve.sh"],
        cmd = """"cat <<'EOF' > $@
{script}
EOF
chmod +x $@
""".format(script = script_content),
    )"

    # Create a sh_binary that runs the generated script
    native.sh_binary(
        name = name,
        srcs = [":" + name + "_serve.sh"],
        data = [":" + site_target_name],
        visibility = ["//visibility:public"],
    )
