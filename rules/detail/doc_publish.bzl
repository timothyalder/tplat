load("@aspect_bazel_lib//lib:run_binary.bzl", "run_binary")
load("@bazel_skylib//rules:write_file.bzl", "write_file")
load("@rules_shell//shell:sh_binary.bzl", "sh_binary")
load(":doc_site_build.bzl", "doc_site_build")

def doc_publish(name, theme = "just-the-docs", skip_validation = False, **kwargs):
    # Build the static site first
    doc_site_build(
        name = name + "_site",
        skip_validation = skip_validation,
        theme = theme,
        **kwargs,
    )
    run_binary(
        name = name + "_site.build",
        srcs = [
            ":" + name + "_site",
        ],
        args = [
            "build",
            "--destination",
            "$(GENDIR)/_site",
            "--config",
            "_config.yml",
        ],
        env = {
            "LC_ALL": "C.UTF-8",
            "LANG": "en_US.UTF-8",
            "LANGUAGE": "en_US.UTF-8",
        },
        execution_requirements = {"no-sandbox": "1"},
        mnemonic = "JekyllBuild",
        out_dirs = [
            "_site",
        ],
        tool = "@bundle//bin:jekyll",
    )

    # Define a separate `bazel run` target for serving
    write_file(
        name = "site_serve_file",
        out = "site_serve_file.sh",
        content = [
            "#!/bin/bash",
            # rules_ruby needs RUNFILES_DIR to be set
            "export RUNFILES_DIR=$(readlink -f ../)",
            "EXEC_ROOT=$(pwd)",
            "$EXEC_ROOT/$1 ${@:2}",
        ],
    )
    sh_binary(
        name = name + "_site.serve",
        srcs = [
            ":site_serve_file",
        ],
        args = [
            "$(location @bundle//bin:jekyll)",
            "serve",
            "--destination",
            "_site",
            "--skip-initial-build",
            "--config",
            "_config.yml",
        ],
        data = [
            ":" + name + "_site.build",
            "@bundle//bin:jekyll",
        ],
    )
