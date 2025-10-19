DOC_SITE_ARGS = {
    "title": attr.string(mandatory = True, doc = "Title of generated site"),
    "index": attr.label(
        allow_single_file = [".md"],
        mandatory = True,
        doc = "Index for the publication",
    ),
    "config": attr.label_list(
        allow_files = True,
        mandatory = False,
        doc = "List of configs that will be applied to Jekyll with latter configs capable of overriding earlier configs",
    ),
    # "themes": attr.label_list(
    #     allow_files = True,
    #     default = ...,
    #     doc = "List of themes that will be applied to Jekyll with latter themes capable of overriding earlier themes",
    # ),
}