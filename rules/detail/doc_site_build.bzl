load(":_deterministic_tar_cmd.bzl", "deterministic_tar_cmd")
load(":_doc_section_args.bzl", "DOC_SECTION_ARGS")
load(":_doc_site_args.bzl", "DOC_SITE_ARGS")
load(":_doc_providers.bzl", "DocSectionInfo")

def _doc_site_build_impl(ctx):
    
    # output_tar = ctx.actions.declare_file(ctx.label.name + ".tar")
    output_dir = ctx.actions.declare_directory(ctx.label.name + ".output")

    sections_strs = []

    for dep in ctx.attr.srcs:
        if DocSectionInfo in dep:
            # Collect this section’s page paths
            paths = [page.file.path for page in dep[DocSectionInfo].site_pages]
            # Join them with commas, wrap in parentheses
            section_str = "(" + ",".join(paths) + ")"
            sections_strs.append(section_str)
        else:
            # If it's just raw files
            paths = [f.path for f in dep.files.to_list()]
            section_str = "(" + ",".join(paths) + ")"
            sections_strs.append(section_str)

    # Combine all sections into one string
    sections_arg = "[" + ",".join(sections_strs) + "]"
    print(sections_arg)

    args = [
        "--title", ctx.attr.title,
        # "--index", ctx.attr.index.path,
        "--sections", sections_arg,
        "--output_dir", output_dir.path,
    ]

    ctx.actions.run(
        inputs = ctx.files.srcs + [ctx.file.index],
        outputs = [output_dir],
        executable = ctx.executable._formatter,
        arguments = args,
        progress_message = "Formatting site sources...",
        use_default_shell_env = True,
    )

    # script.append("cd x && bundle exec jekyll serve")
    # script.append("cp -r \"${{BUILDTMP}/output\"/* \"{output}\"".format(output = output_dir.path))
    # script.append(deterministic_tar_cmd(output_tar.path, "${BUILDTMP}/output"))

    # script_file = ctx.actions.declare_file(ctx.attr.name + ".sh")

    # ctx.actions.write(
    #     output = script_file,
    #     content = "\n".join(script),
    #     is_executable = True,
    # )

    # ctx.actions.run_shell(
    #     command = script_file.path,
    #     arguments = [],
    #     outputs = [output_dir, output_tar],
    #     use_default_shell_env = True,
    #     inputs = depset([script_file], transitive = [site_inputs])
    # )

    # return [
    #     DefaultInfo(
    #         files = depset([output_dir]),
    #         runfiles = ctx.runfiles(transitive_files = site_inputs),
    #     ),
    #     OutputGroupInfo(
    #         tarball = depset([output_dir]),
    #         _validation = depset(validation_outputs)
    #     )
    # ]


doc_site_build = rule(
    attrs = DOC_SECTION_ARGS | DOC_SITE_ARGS | {
        "_formatter": attr.label(
            default = Label("//rules/utils:jekyll_site_formatter"),
            executable = True,
            cfg = "exec",
        ),
    }, 
    # toolchains = ...
    implementation = _doc_site_build_impl,
    doc = "Creates the necessary artefacts for a documentation site"
)