load("//rules/detail:doc_section.bzl", _doc_section = "doc_section")

def doc_section(**kwargs):
    tags = kwargs.pop("tags", [])
    tags.append("docs")
    _doc_section(
        # target_compatible_with = kwargs.pop("target_compatible_with", _TPLATDOC_TARGET_COMPATIBLE_WITH),
        tags = tags,
        **kwargs
    )