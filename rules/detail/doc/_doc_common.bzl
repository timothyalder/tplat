"""Helpers shared between doc_section and doc_site_build."""

load(":_doc_providers.bzl", "DocSectionInfo")

# Generous headroom over the number of doc_section targets that exist in the
# repo today (~40). Starlark forbids recursive function calls, so the tree
# walk below uses an explicit worklist bounded by this constant instead of
# recursing into nested sections.
_MAX_SECTIONS = 2000

_SLUG_CHARS = "abcdefghijklmnopqrstuvwxyz0123456789-"

# The one path segment the docs tree hangs off. Used for both the on-disk
# content layout and the published URLs, which have to agree.
DOCS_SEGMENT = "docs"

def validate_slug(label, slug):
    """Fails unless slug is a non-empty, lowercase, hyphenated URL path segment.

    doc_section directories are named after this value (see
    build_content_manifest), so an invalid slug would leak straight into the
    site's URLs.
    """
    if not slug:
        fail("doc_section %s must specify a non-empty 'slug' (used as its URL path segment)" % label)
    if slug.startswith("-") or slug.endswith("-"):
        fail("doc_section %s: slug '%s' must not start or end with '-'" % (label, slug))
    for ch in slug.elems():
        if ch not in _SLUG_CHARS:
            fail("doc_section %s: slug '%s' must contain only lowercase letters, digits, and hyphens" % (label, slug))

def unique_name(label):
    """Derives a directory-safe, workspace-unique slug from a target label.

    Sibling sections nested under one parent frequently come from different
    packages but share the same target name (e.g. //a/docs and //b/docs are
    both just "docs"), so the slug must be based on the full label, not
    label.name alone.
    """
    return str(label).replace("@@//", "").replace(":", "_").replace("/", "_")

def collect_md_files(ctx):
    """Depset of markdown Files in ctx's own srcs/index plus every nested doc_section's md_files.

    Respects ctx.attr.skip_validation for this target's own files; does not
    cascade skip_validation into nested sections, who decide independently.
    """
    own = [] if ctx.attr.skip_validation else [ctx.file.index] + [
        f
        for f in ctx.files.srcs
        if f.extension == "md"
    ]
    return depset(
        own,
        transitive = [
            dep[DocSectionInfo].md_files
            for dep in ctx.attr.srcs
            if DocSectionInfo in dep
        ],
    )

def page_entry(src, dest, url_dir, weight, index, front = True):
    """Manifest entry for a markdown file the formatter will transform.

    `url_dir` is the section URL the page lives under. A section index owns
    that URL outright; a leaf page's own segment is derived from its H1 by the
    formatter, which is the only thing that reads file contents.

    `ref` is how links address this file: relative links are authored against
    the source tree, so they resolve against workspace-relative paths.
    """
    return {
        "src": src.path,
        "ref": src.short_path,
        "dest": dest,
        "url_dir": url_dir,
        "weight": weight,
        "index": index,
        "front": front,
    }

def asset_entry(src, dest, url):
    """Manifest entry for a file copied verbatim and linkable at `url`."""
    return {
        "src": src.path,
        "ref": src.short_path,
        "dest": dest,
        "url": url,
    }

# Hugo renders these as pages rather than serving them as page resources, so
# inside a content directory they are reachable at "<stem>/" - not under their
# own filename. Anything else (images, PDFs) keeps its name.
_CONTENT_FORMATS = ["html", "htm", "md", "markdown"]

def content_asset_url(url_dir, f):
    """Site URL of a non-markdown file placed in a content directory."""
    if f.extension in _CONTENT_FORMATS:
        return url_dir + f.basename[:-(len(f.extension) + 1)] + "/"
    return url_dir + f.basename

def build_content_manifest(ctx, dest_root, url_root):
    """Walks the whole doc_section tree rooted at ctx.attr.srcs in a single pass.

    Returns (pages, assets, inputs): manifest entries placing every file
    directly at its final nested destination under dest_root, alongside the
    site URL it will be reachable at, plus every File referenced (for action
    inputs).

    Each nested doc_section's own srcs are walked with weight starting at 10
    (step 10), matching doc_section's historical numbering; dest_root's own
    direct srcs (ctx.attr.srcs) are walked with weight starting at 1 (step
    1), matching doc_site_build's historical numbering.
    """
    pages = []
    assets = []
    inputs = []

    # Worklist entries: (children, dest_dir, url_dir, weight, weight_step).
    frames = [(ctx.attr.srcs, dest_root, url_root, 1, 1)]

    done = False
    for _ in range(_MAX_SECTIONS + 1):
        if not frames:
            done = True
            break
        children, dest_dir, url_dir, weight, step = frames.pop()
        seen_slugs = {}
        for child in children:
            if DocSectionInfo in child:
                info = child[DocSectionInfo]
                if info.name in seen_slugs:
                    fail("doc_section slug '%s' is used by more than one section under '%s' - slugs must be unique among siblings" % (info.name, dest_dir))
                seen_slugs[info.name] = True
                child_dir = dest_dir + "/" + info.name
                child_url = url_dir + info.name + "/"
                pages.append(page_entry(info.index, child_dir + "/_index.md", child_url, weight, index = True))
                inputs.append(info.index)
                for f in info.data:
                    assets.append(asset_entry(f, child_dir + "/" + f.basename, content_asset_url(child_url, f)))
                    inputs.append(f)
                frames.append((info.srcs, child_dir, child_url, 10, 10))
            else:
                f = child.files.to_list()[0]
                dest = dest_dir + "/" + f.basename
                if f.extension == "md":
                    pages.append(page_entry(f, dest, url_dir, weight, index = False))
                else:
                    assets.append(asset_entry(f, dest, content_asset_url(url_dir, f)))
                inputs.append(f)
            weight += step

    if not done:
        fail("doc tree has more than %d sections - raise _MAX_SECTIONS in _doc_common.bzl" % _MAX_SECTIONS)

    return pages, assets, inputs
