load(":_doc_providers.bzl", "DocSectionInfo", "DocPageInfo")
load(":_doc_section_args.bzl", "DOC_SECTION_ARGS")

def valid_extension(f):
    if f.extension in ["md"]:
        return True
    return False


def assert_valid_extension(f):
    if not valid_extension(f):
        fail("Error %s is not a valid extension for doc_section. Should be .md" % f.path)


def doc_section_rule(ctx):
    site_pages = []

    if ctx.file.index:
        assert_valid_extension(ctx.file.index)

    for dep in ctx.attr.srcs:
        for f in dep[DocSectionInfo].site_pages:
            page = DocPageInfo(
                file = f.file,
                path = "/".join([str(dep.label).replace("@//","").replace(":","_").replace("/","_"), f.path]),
                data = f.data,
                depth = f.depth + 1
            )
            site_pages.append(page)

    return DocSectionInfo(site_pages=site_pages)


def _doc_section_impl(ctx):
    section, validation_outputs = doc_section_rule(ctx)
    return [
        section,
        OutputGroupInfo(_validation = depset(validation_outputs)),
    ]


doc_section = rule(
    attrs = DOC_SECTION_ARGS,
    implementation = _doc_section_impl,
    doc = "Declares a section which is a nestable chunk of content."
)