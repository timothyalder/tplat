load(":_doc_common.bzl", "collect_md_files", "validate_slug")
load(":_doc_providers.bzl", "DocSectionInfo")
load(":_doc_section_args.bzl", "DOC_SECTION_ARGS")

def _doc_section_impl(ctx):
    validate_slug(ctx.label, ctx.attr.slug)
    return [
        DefaultInfo(),
        DocSectionInfo(
            name = ctx.attr.slug,
            index = ctx.file.index,
            srcs = ctx.attr.srcs,
            data = ctx.files.data,
            md_files = collect_md_files(ctx),
        ),
    ]

doc_section = rule(
    attrs = DOC_SECTION_ARGS,
    implementation = _doc_section_impl,
    doc = "Declares a nestable chunk of content. Produces no build outputs of its own - consumed by doc_site_build, which formats, copies, and lints the whole tree in a single pass.",
)
