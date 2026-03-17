def _markdown_rule_impl(ctx):
    output = ctx.actions.declare_file(ctx.label.name + ".lint")

    args = ctx.actions.args()
    args.add("--recursive")
    for f in ctx.files.srcs:
        args.add(f)

    ctx.actions.run(
        executable = ctx.executable._mdl,
        inputs = ctx.files.srcs,
        outputs = [output],
        arguments = [args],
        mnemonic = "MarkdownLint",
        progress_message = "Linting markdown for {}".format(ctx.label),
    )

    return DefaultInfo(files = depset([output]))

markdown_lint = rule(
    implementation = _markdown_rule_impl,
    attrs = {
        "srcs": attr.label_list(allow_files = [".md"]),
        "_mdl": attr.label(
            default = Label("//rules/detail/mdl:mdl"),
            executable = True,
            cfg = "exec",
        ),
    },
)