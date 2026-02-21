load(":_doc_providers.bzl", "DocSectionInfo", "DocSiteInfo")
load(":_doc_section_args.bzl", "DOC_SECTION_ARGS")
load(":_doc_site_args.bzl", "DOC_SITE_ARGS")

def _doc_site_build_impl(ctx):
    section_files = []
    data_files = []
    weight = 1

    output_dir = ctx.actions.declare_directory("content/docs")
    script = ctx.actions.declare_file(str(ctx.label).replace("@@//", "").replace(":", "_").replace("/", "_") + "_build.sh")
    config = ctx.actions.declare_file("conf/config.yaml")
    formatter = ctx.executable._formatter
    config_tmpl = ctx.file._config_tmpl

    # Collect all doc_sections, markdown files, and data from deps
    script_lines = [
        "#!/usr/bin/env bash",
        "set -euo pipefail",
        "",
        "mkdir -p '{out}'".format(out = output_dir.path),
        "mkdir -p '{out}/data'".format(out = output_dir.path),
        # Declare config
        "cp '{tmpl}' '{config}'".format(
            tmpl = ctx.file._config_tmpl.path,
            config = config.path,
        ),
        "echo '\n  BookDateFormat: {date}\n\ntitle: {title}\ntheme: {theme}\n' >> '{config}'".format(
            date = "20th February 2026",  # TODO: make this resolve dynamically
            title = ctx.attr.title,
            config = config.path,
            theme = ctx.attr.theme,
        ),
        # Copy index file
        "cp '{index}' '{out}/_index.md'".format(index = ctx.file.index.path, out = output_dir.path),
        "",
        "# Copy markdown and data files",
    ]
    for dep in ctx.attr.srcs:
        if DocSectionInfo in dep:
            section = dep[DocSectionInfo].output_dir
            section_files.append(section)
            script_lines.append("'{formatter}' '{src}' '{out}/{file}/' --weight {weight}".format(
                formatter = formatter.path,
                src = section.path,
                out = output_dir.path,
                file = section.basename,
                weight = weight,
            ))
            weight += 1
        else:
            file = dep.files.to_list()[0]  # Hacky
            section_files.append(file)
            script_lines.append("'{formatter}' '{src}' '{out}/{file}' --weight {weight}".format(
                formatter = formatter.path,
                src = file.path,
                out = output_dir.path,
                file = file.basename,
                weight = weight,
            ))
            weight += 1
    for dep in ctx.attr.data:
        for file in dep.files.to_list():
            data_files.append(file)
            script_lines.append("cp '{src}' '{out}/{file}'".format(
                src = file.path,
                out = output_dir.path,
                file = file.basename,
            ))
    deps = [config_tmpl, ctx.file.index] + section_files + data_files
    ctx.actions.write(
        output = script,
        content = "\n".join(script_lines),
        is_executable = True,
    )
    ctx.actions.run(
        inputs = depset(deps),
        outputs = [output_dir, config],
        executable = script,
        tools = [formatter],
        progress_message = "Building doc_section for %s" % ctx.attr.name,
        use_default_shell_env = True,
    )

    return [
        DefaultInfo(
            executable = script,
            files = depset([output_dir, config]),
            runfiles = ctx.runfiles(files = [script]),
        ),
        OutputGroupInfo(
            config = depset([config]),
            files = depset([output_dir]),
        ),
        DocSiteInfo(
            output_dir = output_dir,
        ),
    ]

doc_site_build = rule(
    attrs = DOC_SECTION_ARGS | DOC_SITE_ARGS | {
        "_formatter": attr.label(
            default = "//rules/detail/doc/utils:formatter",
            executable = True,
            cfg = "exec",
        ),
        "_config_tmpl": attr.label(
            default = "//rules/detail/doc/data:config.yaml",
            allow_single_file = True,
        ),
    },
    implementation = _doc_site_build_impl,
    doc = "Creates the necessary folder structure and copies markdown/data files for a documentation site.",
)
