load("//rules/detail:doc_publish.bzl", _doc_publish = "doc_publish")
load("//rules/detail:doc_section.bzl", _doc_section = "doc_section")

def doc_section(**kwargs):
    tags = kwargs.pop("tags", [])
    tags.append("docs")
    _doc_section(
        # target_compatible_with = kwargs.pop("target_compatible_with", _DOC_TARGET_COMPATIBLE_WITH),
        tags = tags,
        **kwargs
    )

def doc_publish(**kwargs):
    tags = kwargs.pop("tags", [])
    tags.append("docs")
    _doc_publish(
        # target_compatible_with = kwargs.pop("target_compatible_with", _DOC_TARGET_COMPATIBLE_WITH),
        tags = tags,
        **kwargs
    )
