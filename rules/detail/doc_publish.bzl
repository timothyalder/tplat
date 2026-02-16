load(":doc_site_build.bzl", "doc_site_build")
load(":doc_site_serve.bzl", "doc_site_serve")

def doc_publish(name, theme = "just-the-docs", skip_validation = False, **kwargs):
    # Build the static site first
    doc_site_build(
        name = name + "_site",
        skip_validation = skip_validation,
        theme = theme,
        **kwargs,
    )

    # Define a separate `bazel run` target for serving
    kwargs.pop("index")
    kwargs.pop("title")
    kwargs.pop("srcs")
    doc_site_serve(
        name = name + "_site.serve",
        site = ":" + name + "_site",
        **kwargs,
    )
