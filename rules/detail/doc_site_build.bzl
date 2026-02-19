load(":_doc_section_args.bzl", "DOC_SECTION_ARGS")
load(":_doc_site_args.bzl", "DOC_SITE_ARGS")
load(":_doc_providers.bzl", "DocSiteInfo")

def _doc_site_build_impl(ctx):
    section_files = []
    data_files = []

    output_dir = ctx.actions.declare_directory("content")
    script = ctx.actions.declare_file(str(ctx.label).replace("@@//","").replace(":","_").replace("/","_") + "_build.sh")

    # Collect all doc_sections, markdown files, and data from deps
    script_lines = [
        "#!/usr/bin/env bash",
        "set -euo pipefail",
        "",
        "mkdir -p '{out}'".format(out=output_dir.path),
        "mkdir -p '{out}/data'".format(out=output_dir.path),
        # Copy index file
        "cp '{index}' '{out}/_index.md'".format(index=ctx.file.index.path, out=output_dir.path),
        "",
        "# Copy markdown and data files",
    ]
    for dep in ctx.attr.srcs:
        if OutputGroupInfo in dep:
            for section in dep.files.to_list():
                section_files.append(section)
                script_lines.append("cp -r '{src}' '{out}/{file}/'".format(
                    src=section.path,
                    out=output_dir.path,
                    file=section.basename,
                ))
        else:
            for file in dep.files.to_list():
                section_files.append(file)
                script_lines.append("cp '{src}' '{out}/{file}'".format(
                    src=file.path,
                    out=output_dir.path,
                    file=file.basename,
                ))
    for dep in ctx.attr.data:
        for file in dep.files.to_list():
            data_files.append(file)
            script_lines.append("cp '{src}' '{out}/data/{file}'".format(
                src=file.path,
                out=output_dir.path,
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
        executable=script,
        progress_message="Building doc_section for %s" % ctx.attr.name,
        use_default_shell_env=True,
    )

    return [
        DefaultInfo(
            executable = script,
            runfiles = ctx.runfiles(files = [script]),
            files=depset([output_dir]),
        ),
        DocSiteInfo(
            output_dir = output_dir,
        ),
    ]

doc_site_build = rule(
    attrs = DOC_SECTION_ARGS | DOC_SITE_ARGS,
    implementation = _doc_site_build_impl,
    doc = "Creates the necessary folder structure and copies markdown/data files for a documentation site.",
)
