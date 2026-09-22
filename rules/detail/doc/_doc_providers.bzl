DocSiteInfo = provider(
    fields = {
        "content_dir": "Directory containing site content",
        "static_dir": "Directory containing site static data",
        "config": "config.yaml for site",
    },
)
DocSectionInfo = provider(
    fields = {
        "name": "Unique directory slug for this section, derived from its label",
        "index": "File: this section's own index markdown, untransformed",
        "srcs": "List of Target: this section's own srcs (nested doc_section deps or leaf markdown file deps), in declared order",
        "data": "List of File: data files to place alongside this section's content, copied untransformed",
        "md_files": "Depset of File: markdown files in this section and its nested subtree eligible for linting (respects skip_validation)",
    },
)

DocMenuItem = provider(
    fields = {
        "name": "Name displayed in menu",
        "url": "URL menu item links to",
        "pageRef": "Relative page reference item links to",
        "weight": "Weight of menu item",
        "data": "Files to include when building DocMenuItem",
    }
)
