load(":_doc_common.bzl", "build_content_script", "collect_md_files", "unique_name")
load(":_doc_providers.bzl", "DocMenuItem", "DocSiteInfo")
load(":_doc_section_args.bzl", "DOC_SECTION_ARGS")
load(":_doc_site_args.bzl", "DOC_SITE_ARGS")

def _doc_site_build_impl(ctx):
    static_files = []
    data_files = []

    name = unique_name(ctx.label)
    content_dir = ctx.actions.declare_directory("content")
    static_dir = ctx.actions.declare_directory("static")
    script = ctx.actions.declare_file(name + "_build.sh")
    config = ctx.actions.declare_file("conf/config.yaml")
    lint_stamp = ctx.actions.declare_file(name + "_lint.ok")
    formatter = ctx.executable._formatter
    linter = ctx.executable.linter
    linter_config = ctx.file.linter_config
    config_tmpl = ctx.file._config_tmpl

    # Single pass over every markdown file in the whole tree.
    md_files = collect_md_files(ctx)
    md_files_list = md_files.to_list()
    lint_script = ctx.actions.declare_file(name + "_lint.sh")
    ctx.actions.write(
        output = lint_script,
        content = "\n".join([
            "#!/usr/bin/env bash",
            "set -euo pipefail",
            "",
            "'{linter}' -c '{config}' {files}".format(
                linter = linter.path,
                config = linter_config.path,
                files = " ".join(["'%s'" % f.path for f in md_files_list]),
            ),
            "",
            "touch '{stamp}'".format(stamp = lint_stamp.path),
        ]),
        is_executable = True,
    )
    ctx.actions.run(
        inputs = depset(md_files_list + [linter_config]),
        outputs = [lint_stamp],
        tools = [linter],
        executable = lint_script,
        progress_message = "Linting docs for %s" % ctx.attr.name,
        use_default_shell_env = True,
        env = {
            "BAZEL_BINDIR": "."
        }
    )

    # Single pass over every file in the whole tree, writing each directly to
    # its final nested destination.
    content_script_lines, content_inputs, mkdirs = build_content_script(
        ctx,
        formatter,
        content_dir.path + "/docs",
    )

    script_lines = [
        "#!/usr/bin/env bash",
        "set -euo pipefail",
        "",
        "mkdir -p '{out}'".format(out = content_dir.path),
        "mkdir -p '{out}'".format(out = static_dir.path),
        "cp '{tmpl}' '{config}'".format(
            tmpl = config_tmpl.path,
            config = config.path,
        ),
        "echo '\n  BookDateFormat: {date}\n\ntitle: {title}\ntheme: {theme}\n' >> '{config}'".format(
            date = "20th February 2026",  # TODO: make this resolve dynamically
            title = ctx.attr.title,
            config = config.path,
            theme = ctx.attr.theme,
        ),
        "echo 'menu:\n  after:' >> '{config}'".format(
            config = config.path,
        ),
        "cp '{index}' '{out}/_index.md'".format(index = ctx.file.index.path, out = content_dir.path),
    ]
    for doc_menu_item in ctx.attr.menu:
        doc_menu_item = doc_menu_item[DocMenuItem]
        for dep in doc_menu_item.data:
            for file in dep.files.to_list():
                static_files.append(file)
                script_lines.append("cp '{src}' '{out}/{file}'".format(
                    src = file.path,
                    out = static_dir.path,
                    file = file.basename,
                ))
        script_lines.append(
            "echo '    - name: \"{name}\"\n      {link}: \"{dest}\"\n      weight: {weight}' >> '{config}'".format(
                name = doc_menu_item.name,
                link = "url" if doc_menu_item.url else "pageRef",
                dest = doc_menu_item.url if doc_menu_item.url else doc_menu_item.pageRef,
                weight = doc_menu_item.weight,
                config = config.path,
            ),
        )
    for dir in mkdirs:
        script_lines.append("mkdir -p '{dir}'".format(dir = dir))
    script_lines.extend(content_script_lines)
    for dep in ctx.attr.data:
        for file in dep.files.to_list():
            data_files.append(file)
            script_lines.append("cp '{src}' '{out}/{file}'".format(
                src = file.path,
                out = static_dir.path,
                file = file.basename,
            ))
    deps = [config_tmpl, ctx.file.index, lint_stamp] + content_inputs + data_files + static_files
    ctx.actions.write(
        output = script,
        content = "\n".join(script_lines),
        is_executable = True,
    )
    ctx.actions.run(
        inputs = depset(deps),
        outputs = [content_dir, config, static_dir],
        executable = script,
        tools = [formatter],
        progress_message = "Building doc_section for %s" % ctx.attr.name,
        use_default_shell_env = True,
        env = {
            "BAZEL_BINDIR": '.'
        }
    )

    return [
        DefaultInfo(
            executable = script,
            files = depset([content_dir, config, static_dir]),
            runfiles = ctx.runfiles(files = [script]),
        ),
        OutputGroupInfo(
            config = depset([config]),
            files = depset([content_dir]),
            static = depset([static_dir]),
            lint = depset([lint_stamp]),
        ),
        DocSiteInfo(
            content_dir = content_dir,
            static_dir = static_dir,
            config = config,
        ),
    ]

doc_site_build = rule(
    attrs = DOC_SECTION_ARGS | DOC_SITE_ARGS | {
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
        "_config_tmpl": attr.label(
            default = "//rules/detail/doc/data:config.yaml",
            allow_single_file = True,
        ),
    },
    implementation = _doc_site_build_impl,
    doc = "Creates the necessary folder structure and copies markdown/data files for a documentation site, formatting and linting the whole nested doc_section tree in a single pass.",
)
