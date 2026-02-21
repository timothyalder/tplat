DOC_SITE_ARGS = {
    "title": attr.string(mandatory = True, doc = "Title of generated site"),
    "index": attr.label(
        allow_single_file = [".md"],
        mandatory = True,
        doc = "Index for the publication",
    ),
    "theme": attr.string(
        default = "just-the-docs",
        doc = "Theme to be applied to Jekyll site",
    ),
}
