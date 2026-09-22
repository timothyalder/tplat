"""Helpers shared between doc_section and doc_site_build."""

load(":_doc_providers.bzl", "DocSectionInfo")

# Generous headroom over the number of doc_section targets that exist in the
# repo today (~40). Starlark forbids recursive function calls, so the tree
# walk below uses an explicit worklist bounded by this constant instead of
# recursing into nested sections.
_MAX_SECTIONS = 2000

_SLUG_CHARS = "abcdefghijklmnopqrstuvwxyz0123456789-"

def validate_slug(label, slug):
    """Fails unless slug is a non-empty, lowercase, hyphenated URL path segment.

    doc_section directories are named after this value (see build_content_script),
    so an invalid slug would leak straight into the site's URLs.
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

def _transform_cmd(formatter, src, dest, weight):
    return "'{formatter}' '{src}' '{dest}' --weight {weight}".format(
        formatter = formatter.path,
        src = src.path,
        dest = dest,
        weight = weight,
    )

def _copy_cmd(src, dest):
    return "cp '{src}' '{dest}'".format(src = src.path, dest = dest)

def build_content_script(ctx, formatter, dest_root):
    """Walks the whole doc_section tree rooted at ctx.attr.srcs in a single pass.

    Returns (script_lines, inputs, mkdirs):
      - script_lines: formatter/cp commands to assemble every file directly
        at its final nested destination path under dest_root.
      - inputs: every File referenced by script_lines (for action inputs).
      - mkdirs: every destination directory that must exist before
        script_lines runs (including dest_root itself).

    Each nested doc_section's own srcs are walked with weight starting at 10
    (step 10), matching doc_section's historical numbering; dest_root's own
    direct srcs (ctx.attr.srcs) are walked with weight starting at 1 (step
    1), matching doc_site_build's historical numbering.
    """
    script_lines = []
    inputs = []
    mkdirs = [dest_root]

    # Worklist entries: (children, dest_dir, weight, weight_step).
    frames = [(ctx.attr.srcs, dest_root, 1, 1)]

    done = False
    for _ in range(_MAX_SECTIONS + 1):
        if not frames:
            done = True
            break
        children, dest_dir, weight, step = frames.pop()
        seen_slugs = {}
        for child in children:
            if DocSectionInfo in child:
                info = child[DocSectionInfo]
                if info.name in seen_slugs:
                    fail("doc_section slug '%s' is used by more than one section under '%s' - slugs must be unique among siblings" % (info.name, dest_dir))
                seen_slugs[info.name] = True
                child_dir = dest_dir + "/" + info.name
                mkdirs.append(child_dir)
                script_lines.append(_transform_cmd(formatter, info.index, child_dir + "/_index.md", weight))
                inputs.append(info.index)
                for f in info.data:
                    script_lines.append(_copy_cmd(f, child_dir + "/" + f.basename))
                    inputs.append(f)
                frames.append((info.srcs, child_dir, 10, 10))
            else:
                f = child.files.to_list()[0]
                script_lines.append(_transform_cmd(formatter, f, dest_dir + "/" + f.basename, weight))
                inputs.append(f)
            weight += step

    if not done:
        fail("doc tree has more than %d sections - raise _MAX_SECTIONS in _doc_common.bzl" % _MAX_SECTIONS)

    return script_lines, inputs, mkdirs
