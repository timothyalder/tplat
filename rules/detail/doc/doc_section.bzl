load(":_doc_providers.bzl", "DocSectionInfo")
load(":_doc_section_args.bzl", "DOC_SECTION_ARGS")

def _doc_section_impl(ctx):
    section_files = []
    data_files = []
    weight = 10

    output_dir = ctx.actions.declare_directory(str(ctx.label).replace("@@//", "").replace(":", "_").replace("/", "_") + ".output")
    script = ctx.actions.declare_file(str(ctx.label).replace("@@//", "").replace(":", "_").replace("/", "_") + "_build.sh")
    formatter = ctx.executable._formatter
    linter = ctx.executable.linter
    linter_config = ctx.file.linter_config
    md_files = [ctx.file.index] + [f for f in ctx.files.srcs if f.extension == "md"]

    script_lines = [
        "#!/usr/bin/env bash",
        "set -euo pipefail",
        "",
        "'{linter}' -c '{config}' {files}".format(
            linter = linter.path,
            config = linter_config.path,
            files = " ".join(["'%s'" % f.path for f in md_files]),
        ),
        "",
        "mkdir -p '{output}'".format(output = output_dir.path),
        "mkdir -p '{output}/data'".format(output = output_dir.path),
        "'{formatter}' '{index}' '{output}/_index.md'".format(formatter = formatter.path, index = ctx.file.index.path, output = output_dir.path),
        "",
        "# Copy markdown and data files",
    ]
    for dep in ctx.attr.srcs:
        if DocSectionInfo in dep:
            section = dep[DocSectionInfo].output_dir
            section_files.append(section)
            script_lines.append("'{formatter}' '{src}' '{output}/{file}/' --weight {weight}".format(
                formatter = formatter.path,
                src = section.path,
                output = output_dir.path,
                file = section.basename,
                weight = weight,
            ))
            weight += 10
        else:
            file = dep.files.to_list()[0]
            section_files.append(file)
            script_lines.append("'{formatter}' '{src}' '{output}/{file}' --weight {weight}".format(
                formatter = formatter.path,
                src = file.path,
                output = output_dir.path,
                file = file.basename,
                weight = weight,
            ))
            weight += 10
    for dep in ctx.attr.data:
        for file in dep.files.to_list():
            data_files.append(file)
            script_lines.append("cp '{src}' '{output}/{file}'".format(
                src = file.path,
                output = output_dir.path,
                file = file.basename,
            ))
    deps = [ctx.file.index, linter_config] + section_files + data_files
    ctx.actions.write(
        output = script,
        content = "\n".join(script_lines),
        is_executable = True,
    )
    ctx.actions.run(
        inputs = depset(deps),
        outputs = [output_dir],
        tools = [formatter, linter],
        executable = script,
        progress_message = "Building doc_section for %s" % ctx.attr.name,
        use_default_shell_env = True,
        env = {
            "BAZEL_BINDIR": '.'
        }
    )

    return [
        DefaultInfo(
            executable = script,
            runfiles = ctx.runfiles(files = [script]),
            files = depset([output_dir]),
        ),
        DocSectionInfo(output_dir = output_dir),
    ]

doc_section = rule(
    attrs = DOC_SECTION_ARGS | {
        "_formatter": attr.label(
            default = "//rules/detail/doc/utils:formatter",
            executable = True,
            cfg = "exec",
        ),
        "linter": attr.label(
            default = "//rules/detail/markdownlint_cli:markdownlint_cli",
            executable = True,
            cfg = "exec",
        ),
        "linter_config": attr.label(
            default = "//rules/detail/markdownlint_cli:style_json",
            allow_single_file = True,
        ),
    },
    implementation = _doc_section_impl,
    doc = "Declares a section which is a nestable chunk of content.",
)
