load(":doc_site_build.bzl", "doc_site_build")
load(":doc_site_serve.bzl", "doc_site_serve")

def doc_publish(name, config = [], skip_validation = False, **kwargs):
    # Build the static site first
    doc_site_build(
        name = name + "_site",
        config = config,
        skip_validation = skip_validation,
        **kwargs
    )
    # ctx.actions.declare_directory(str(ctx.label).replace("@@//","").replace(":","_").replace("/","_") + ".output")
    site_dir = name

    # Define a separate `bazel run` target for serving
    # kwargs.pop("index")
    # kwargs.pop("title")
    doc_site_serve(
        name = name + "_site.serve",
        site_dir = site_dir,
        # **kwargs
    )
