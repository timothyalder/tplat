DOC_SECTION_ARGS = {
    "srcs": attr.label_list(allow_files = True, doc = "List of markdown files or <a href=\"#doc_section\">doc_section</a>'s."),
    "data": attr.label_list(allow_files = True, doc = "List of files needed by the included markdown files - e.g., images."),
    "skip_validation": attr.bool(default = False, doc = "Skip validation")
}