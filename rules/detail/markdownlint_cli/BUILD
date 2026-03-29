load("@npm//:markdownlint-cli/package_json.bzl", markdownlint_bin = "bin")

exports_files([
    "style.json",
])

genrule(
    name = "debug_bin",
    outs = ["bin.txt"],
    cmd = """
    echo "{bin}" > $@
    """.format(bin = markdownlint_bin),
)
