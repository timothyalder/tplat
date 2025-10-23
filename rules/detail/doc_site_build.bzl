load(":_doc_providers.bzl", "DocSectionInfo")
load(":_doc_section_args.bzl", "DOC_SECTION_ARGS")
load(":_doc_site_args.bzl", "DOC_SITE_ARGS")

def _normalize_path(path):
    # Drop the file name (everything after the last slash)
    if "/" in path:
        path = path.rsplit("/", 1)[0]
    else:
        return ""  # No directories, just a filename

    # Replace remaining slashes with underscores
    return path.replace("/", "_")

def _doc_site_build_impl(ctx):
    site_name = ctx.attr.name
    output_dir = ctx.actions.declare_directory(site_name + ".output")

    # Collect markdown and data files from all deps
    section_files = []
    data_files = []

    for dep in ctx.attr.srcs:
        if DocSectionInfo in dep:
            section_info = dep[DocSectionInfo]
            for page in section_info.site_pages:
                section_files.append(page.file)
                if page.data:
                    data_files.extend(page.data)
        else:
            section_files.extend(dep.files.to_list())

    # Generate a shell script to perform the copy/layout operations.
    script = ctx.actions.declare_file(site_name + "_build.sh")

    script_lines = [
        "#!/usr/bin/env bash",
        "set -euo pipefail",
        "",
        # Create root folder
        "mkdir -p '{output}'".format(output=output_dir.path),
        # Copy index file
        "cp '{index}' '{output}/'".format(index=ctx.file.index.path, output=output_dir.path),
        "",
        "# Copy markdown and data files",
    ]

    # Copy section markdown files
    for f in section_files:
        # Compute the subfolder name (based on original relative path)
        dest_rel = f.short_path
        script_lines.append("mkdir -p '{output}/{dest_dir}'".format(
            output=output_dir.path,
            dest_dir=_normalize_path(dest_rel),
        ))
        script_lines.append("cp '{src}' '{output}/{dest_dir}/'".format(
            src=f.path,
            output=output_dir.path,
            dest_dir=_normalize_path(dest_rel),
        ))

    # Copy data files
    for d in data_files:
        dest_rel = d.short_path
        script_lines.append("mkdir -p '{output}/{dest_dir}'".format(
            output=output_dir.path,
            dest_dir=_normalize_path(dest_rel),
        ))
        script_lines.append("cp '{src}' '{output}/{dest_dir}/'".format(
            src=d.path,
            output=output_dir.path,
            dest_dir=_normalize_path(dest_rel),
        ))

    ctx.actions.write(
        output=script,
        content="\n".join(script_lines),
        is_executable=True,
    )

    ctx.actions.run(
        inputs=depset([ctx.file.index] + section_files + data_files),
        outputs=[output_dir],
        executable=script,
        progress_message="Building documentation site layout for %s" % site_name,
        use_default_shell_env=True,
    )

    return [
        DefaultInfo(files=depset([output_dir])),
    ]

doc_site_build = rule(
    attrs = DOC_SECTION_ARGS | DOC_SITE_ARGS | {
        "_formatter": attr.label(
            default = Label("//rules/utils:jekyll_site_formatter"),
            executable = True,
            cfg = "exec",
        ),
    },
    implementation = _doc_site_build_impl,
    doc = "Creates the necessary folder structure and copies markdown/data files for a documentation site.",
)
