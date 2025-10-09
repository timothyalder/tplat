load(":_doc_section_args.bzl", "DOC_SECTION_ARGS")
load(":_doc_site_args.bzl", "DOC_SITE_ARGS")

def _doc_site_build_impl(ctx):
    


doc_site_build = rule(
    attrs = DOC_SECTION_ARGS | DOC_SITE_ARGS, 
    # toolchains = ...
    implementation = _doc_site_build_impl,
    doc = "Creates the necessary artefacts for a documentation site"
)