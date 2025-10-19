load(":doc_site_build.bzl", "doc_site_build")

def doc_publish(name, config = [], skip_validation = False, **kwargs):
    # In the future, publishing for other mediums (e.g., PDF, localhost, etc. could be added here)

    # Build Jekyll site artefacts
    doc_site_build(
        name = name + "_site",
        config = config,
        skip_validation = skip_validation,
        **kwargs
    )

    # If you call bazel run //projects/docs:docs._site, jekyll serve is run and the published sections 
    # are available at http://localhost:4000
    native.filegroup(
        name = name,
        srcs = [
            ":" + name + "_site",
        ]
    )