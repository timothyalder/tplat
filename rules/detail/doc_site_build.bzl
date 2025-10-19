load(":_deterministic_tar_cmd.bzl", "deterministic_tar_cmd")
load(":_doc_section_args.bzl", "DOC_SECTION_ARGS")
load(":_doc_site_args.bzl", "DOC_SITE_ARGS")
load(":_doc_providers.bzl", "DocSectionInfo")

def _doc_site_build_impl(ctx):
    output_dir = ctx.actions.declare_directory(ctx.label.name + ".output")

    section_files = []
    data_files = []

    # Collect markdowns + associated data
    for dep in ctx.attr.srcs:
        if DocSectionInfo in dep:
            section_info = dep[DocSectionInfo]
            for page in section_info.site_pages:
                section_files.append(page.file)
                if page.data:
                    data_files.extend(page.data)
        else:
            # Fallback for plain files
            section_files.extend(dep.files.to_list())

    args = ctx.actions.args()
    args.add("--title", ctx.attr.title)
    args.add("--index", ctx.file.index.path)
    args.add("--output_dir", output_dir.path)

    for f in section_files:
        args.add("--section", f.path)

    for d in data_files:
        args.add("--data", d.path)

    all_inputs = depset([ctx.file.index] + section_files + data_files)

    ctx.actions.run(
        inputs = all_inputs,
        outputs = [output_dir],
        executable = ctx.executable._formatter,
        arguments = [args],
        progress_message = "Formatting documentation site sources...",
        use_default_shell_env = True,
    )

    return [
        DefaultInfo(files = depset([output_dir]))
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
    doc = "Creates the necessary artefacts for a documentation site",
)
