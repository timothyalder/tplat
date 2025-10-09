load(":doc_section.bzl", "doc_section")

def doc_publish(name, config = [], skip_validation = False, **kwargs)
    # In the future, publishing for other mediums (e.g., PDF, localhost, etc. could be added here)

    doc_site_build(
        name = name + "_site",
        config = config,
        skip_validation = skip_validation,
        **kwargs
    )