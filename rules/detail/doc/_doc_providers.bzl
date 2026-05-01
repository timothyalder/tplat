DocSiteInfo = provider(
    fields = {
        "output_dir": "Directory containing built site",
    },
)
DocSectionInfo = provider(
    fields = {
        "output_dir": "Directory containing built section",
    },
)

DocMenuItem = provider(
    fields = {
        "name": "Name displayed in menu",
        "url": "URL menu item links to",
        "weight": "Weight of menu item",
    }
)
