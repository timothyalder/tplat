load(":_doc_providers.bzl", "DocPageInfo", "DocSectionInfo")
load(":_doc_section_args.bzl", "DOC_SECTION_ARGS")

def valid_extension(f):
    if f.extension in ["md"]:
        return True
    return False

def assert_valid_extension(f):
    if not valid_extension(f):
        fail("Error %s is not a valid extension for doc_section. Should be .md" % f.path)

def doc_section_rule(ctx):
    validation_outputs = []

    def validate_page(page):
        validation_output = ctx.actions.declare_file(("/".join([ctx.attr.name, page.path])))

        # TODO: Run a lint checker
        ctx.actions.write(
            output = validation_output,
            content = "validated: %s" % page.path,
        )

        validation_outputs.append(validation_output)

    # In the future, could have pdf_pages
    site_pages = []

    for dep in ctx.attr.srcs:
        # Enable recursion (doc_section target in doc_section srcs)
        if DocSectionInfo in dep:
            for f in dep[DocSectionInfo].site_pages:
                page = DocPageInfo(
                    file = f.file,
                    path = "/".join([str(dep.label).replace("@//", "").replace(":", "_").replace("/", "_"), f.path]),
                    data = f.data,
                    depth = f.depth + 1,
                )
                site_pages.append(page)
        else:
            for f in dep.files.to_list():
                page = DocPageInfo(
                    file = f,
                    path = "/".join([f.basename]),
                    data = ctx.files.data,
                    depth = 2,
                )
                site_pages.append(page)

                if not ctx.attr.skip_validation:
                    validate_page(page)

    return (DocSectionInfo(site_pages = site_pages), validation_outputs)

def _doc_section_impl(ctx):
    section, validation_outputs = doc_section_rule(ctx)
    return [
        section,
        OutputGroupInfo(_validation = depset(validation_outputs)),
    ]

doc_section = rule(
    attrs = DOC_SECTION_ARGS,
    implementation = _doc_section_impl,
    doc = "Declares a section which is a nestable chunk of content.",
)
