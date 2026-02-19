load("@build_stack_rules_hugo//hugo:rules.bzl", "hugo_site", "hugo_theme", "hugo_serve")
load(":doc_site_build.bzl", "doc_site_build")

def doc_publish(name, theme = "just-the-docs", skip_validation = False, **kwargs):
    doc_site_build(
        name = name + "_site.prepare",
        skip_validation = skip_validation,
        theme = theme,
        **kwargs,
    )

    hugo_theme(
        name = "book",
        srcs = [
            "@com_github_alex_shpak_hugo_book//:files",
        ],
    )

    hugo_site(
        name = name + "_site.build",
        config = "//rules/detail:config.yaml",
        content = [":" + name + "_site.prepare"],
        # static = glob(["static/**"]),
        # layouts = glob(["layouts/**"]),
        theme = ":book",
    )

    hugo_serve(
        name = name + "_site.serve",
        dep = [":" + name + "_site.build"],
        quiet = False, # Bugged https://github.com/stackb/rules_hugo/blob/294a8ec626a394011d35397108c930be631ab9fa/hugo/internal/hugo_site.bzl#L247-L248
    )
