DOC_SITE_ARGS = {
    "title": attr.string(mandatory = True, doc = "Title of generated site"),
    "config": attr.label_list(
        allow_files = True,
        mandatory = False,
        doc = "List of configs that will be appleid to Jekyll with latter configs capable of overriding earlier configs",
    ),
    # "themes": attr.label_list(
    #     allow_files = True,
    #     default = ...,
    #     doc = "List of themes that will be applied to Jekyll with latter themes capable of overriding earlier themes",
    # ),
}