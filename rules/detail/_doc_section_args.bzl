DOC_SECTION_ARGS = {
    "srcs": attr.label_list(allow_files = True, doc = "List of markdown files or <a href=\"#doc_section\">doc_section</a>'s."),
    "data": attr.label_list(allow_files = True, doc = "List of files needed by the included markdown files - e.g., images."),
    "index": attr.label(allow_single_file = [".md"], mandatory = True, doc = "Markdown file to be used for landing page of section."),
    "skip_validation": attr.bool(default = False, doc = "Skip validation"),
}
