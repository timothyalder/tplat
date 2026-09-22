DOC_SECTION_ARGS = {
    "srcs": attr.label_list(allow_files = True, doc = "List of markdown files or <a href=\"#doc_section\">doc_section</a>'s."),
    "data": attr.label_list(allow_files = True, doc = "List of files needed by the included markdown files - e.g., images."),
    "index": attr.label(allow_single_file = [".md"], mandatory = True, doc = "Markdown file to be used for landing page of section."),
    "skip_validation": attr.bool(default = False, doc = "Exclude this section's own markdown files from the site-wide lint pass. Does not affect nested sections, which decide independently via their own skip_validation."),
    "slug": attr.string(default = "", doc = "URL path segment for this section, e.g. \"attack-trees\". Required (lowercase letters, digits, and hyphens only) and must be unique among sibling srcs - it becomes the on-disk directory name under its parent, which is what actually determines the section's URL in Hugo (front-matter slug is a documented no-op for _index.md branch bundles: https://github.com/gohugoio/hugo/issues/7124)."),
}
