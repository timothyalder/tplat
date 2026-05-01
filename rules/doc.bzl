load("//rules/detail/doc:doc_publish.bzl", _doc_publish = "doc_publish")
load("//rules/detail/doc:doc_section.bzl", _doc_section = "doc_section")
load("//rules/detail/doc:doc_menu_item.bzl", _doc_menu_item = "doc_menu_item")

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

doc_menu_item = _doc_menu_item
