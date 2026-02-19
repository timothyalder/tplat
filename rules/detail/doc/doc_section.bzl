load(":_doc_section_args.bzl", "DOC_SECTION_ARGS")

def valid_extension(f):
    if f.extension in ["md"]:
        return True
    return False

def assert_valid_extension(f):
    if not valid_extension(f):
        fail("Error %s is not a valid extension for doc_section. Should be .md" % f.path)

def _doc_section_impl(ctx):

    section_files = []
    data_files = []

    output_dir = ctx.actions.declare_directory(str(ctx.label).replace("@@//","").replace(":","_").replace("/","_") + ".output")
    script = ctx.actions.declare_file(str(ctx.label).replace("@@//","").replace(":","_").replace("/","_") + "_build.sh")
    formatter = ctx.executable._formatter

    # Collect all doc_sections, markdown files, and data from deps
    script_lines = [
        "#!/usr/bin/env bash",
        "set -euo pipefail",
        "",
        "mkdir -p '{output}'".format(output=output_dir.path),
        "mkdir -p '{output}/data'".format(output=output_dir.path),
        # Copy index file
        "'{formatter}' '{index}' '{output}/_index.md'".format(formatter = formatter.path, index=ctx.file.index.path, output=output_dir.path),
        # "cp '{index}' '{output}/_index.md'".format(index=ctx.file.index.path, output=output_dir.path),
        "",
        "# Copy markdown and data files",
    ]
    for dep in ctx.attr.srcs:
        # Enable recursion (doc_section target in doc_section srcs)
        if OutputGroupInfo in dep:
            for section in dep.files.to_list():
                section_files.append(section)
                script_lines.append("cp -r '{src}' '{output}/{file}/'".format(
                    src=section.path,
                    output=output_dir.path,
                    file=section.basename,
                ))
        else:
            for file in dep.files.to_list():
                section_files.append(file)
                assert_valid_extension(file)
                script_lines.append("'{formatter}' '{src}' '{output}/{file}'".format(
                    formatter = formatter.path,
                    src = file.path,
                    output=output_dir.path,
                    file = file.basename,
                ))
    for dep in ctx.attr.data:
        for file in dep.files.to_list():
            data_files.append(file)
            script_lines.append("cp '{src}' '{output}/data/{file}'".format(
                src=file.path,
                output=output_dir.path,
                file=file.basename,
            ))
    deps = [ctx.file.index] + section_files + data_files
    ctx.actions.write(
        output=script,
        content="\n".join(script_lines),
        is_executable=True,
    )
    ctx.actions.run(
        inputs = depset(deps),
        outputs=[output_dir],
        tools=[formatter],
        executable=script,
        progress_message="Building doc_section for %s" % ctx.attr.name,
        use_default_shell_env=True,
    )

    return [
        DefaultInfo(
            executable = script,
            runfiles = ctx.runfiles(files = [script]),
            files = depset([output_dir])
        ),
        OutputGroupInfo(files = depset([output_dir])) # Can do 'file' instead of 'files'?
    ]

doc_section = rule(
    attrs = DOC_SECTION_ARGS | {
        "_formatter": attr.label(
            default = "//rules/detail/doc/utils:formatter",
            executable = True,
            cfg = "exec",
        ),
    },
    implementation = _doc_section_impl,
    doc = "Declares a section which is a nestable chunk of content.",
)
