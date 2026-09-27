load(":_doc_common.bzl", "DOCS_SEGMENT", "asset_entry", "build_content_manifest", "collect_md_files", "page_entry", "unique_name")
load(":_doc_providers.bzl", "DocMenuItem", "DocSiteInfo")
load(":_doc_section_args.bzl", "DOC_SECTION_ARGS")
load(":_doc_site_args.bzl", "DOC_SITE_ARGS")

def _doc_site_build_impl(ctx):
    name = unique_name(ctx.label)
    content_dir = ctx.actions.declare_directory("content")
    static_dir = ctx.actions.declare_directory("static")
    config = ctx.actions.declare_file("conf/config.yaml")
    lint_stamp = ctx.actions.declare_file(name + "_lint.ok")
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

    # Single pass over every file in the whole tree, recording where each one
    # lands and the URL it becomes reachable at. The formatter needs the whole
    # tree at once: a link into another section can only be resolved once the
    # page it points at has been read.
    pages, assets, inputs = build_content_manifest(
        ctx,
        content_dir.path + "/" + DOCS_SEGMENT,
        "/" + DOCS_SEGMENT + "/",
    )

    # The site index is the repo README, published at the site root. It keeps
    # its own heading rather than being given docs front matter, since it is
    # the landing page rather than a page in the docs menu.
    pages.append(page_entry(
        ctx.file.index,
        content_dir.path + "/_index.md",
        "/",
        0,
        index = True,
        front = False,
    ))
    inputs.append(ctx.file.index)

    static_srcs = []
    for dep in ctx.attr.data:
        static_srcs.extend(dep.files.to_list())
    for doc_menu_item in ctx.attr.menu:
        for dep in doc_menu_item[DocMenuItem].data:
            static_srcs.extend(dep.files.to_list())
    for f in static_srcs:
        assets.append(asset_entry(f, static_dir.path + "/" + f.basename, "/" + f.basename))
        inputs.append(f)

    manifest = ctx.actions.declare_file(name + "_manifest.json")
    ctx.actions.write(
        output = manifest,
        content = json.encode({
            "roots": [content_dir.path, static_dir.path],
            "pages": pages,
            "assets": assets,
        }),
    )
    ctx.actions.run(
        inputs = depset(inputs + [manifest, lint_stamp]),
        outputs = [content_dir, static_dir],
        executable = ctx.attr._formatter[DefaultInfo].files_to_run,
        arguments = [manifest.path],
        progress_message = "Assembling doc content for %s" % ctx.attr.name,
        use_default_shell_env = True,
        env = {
            "BAZEL_BINDIR": "."
        }
    )

    config_script = ctx.actions.declare_file(name + "_config.sh")
    config_lines = [
        "#!/usr/bin/env bash",
        "set -euo pipefail",
        "",
        "mkdir -p '{dir}'".format(dir = config.dirname),
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
    ]
    for doc_menu_item in ctx.attr.menu:
        doc_menu_item = doc_menu_item[DocMenuItem]
        config_lines.append(
            "echo '    - name: \"{name}\"\n      {link}: \"{dest}\"\n      weight: {weight}' >> '{config}'".format(
                name = doc_menu_item.name,
                link = "url" if doc_menu_item.url else "pageRef",
                dest = doc_menu_item.url if doc_menu_item.url else doc_menu_item.pageRef,
                weight = doc_menu_item.weight,
                config = config.path,
            ),
        )
    ctx.actions.write(
        output = config_script,
        content = "\n".join(config_lines),
        is_executable = True,
    )
    ctx.actions.run(
        inputs = depset([config_tmpl]),
        outputs = [config],
        executable = config_script,
        progress_message = "Writing Hugo config for %s" % ctx.attr.name,
        use_default_shell_env = True,
    )

    return [
        DefaultInfo(
            files = depset([content_dir, config, static_dir]),
        ),
        OutputGroupInfo(
            config = depset([config]),
            content = depset([content_dir]),
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
