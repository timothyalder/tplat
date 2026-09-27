import os
import tempfile
import unittest

import formatter

# Stands in for the map the manifest produces, using real paths and URLs from
# the docs tree so the traversals under test are the ones authors actually
# write.
URLS = {
    "projects/threat_modelling/docs/index.md": "/docs/threat-modelling/",
    "projects/threat_modelling/docs/identify/eop.md": "/docs/threat-modelling/identify/elevation-of-privlege/",
    "projects/threat_modelling/docs/identify/attack_trees/irl.md": "/docs/threat-modelling/identify/attack-trees/in-real-life/",
    "projects/threat_modelling/docs/identify/attack_trees/data/election.png": "/docs/threat-modelling/identify/attack-trees/election.png",
    "projects/cryptography/cryptography/asymmetric/docs/index.md": "/docs/cryptography/asymmetric-cryptography/",
    "projects/networking/docs/analysis/tools/data/target.html": "/docs/networking/network-traffic-analysis/tools/target/",
    "projects/fpga/docs/mux.md": "/docs/fpga/1-bit-mux/",
    "projects/research/bushfire.pdf": "/docs/research/bushfire.pdf",
}


def rewrite(text, ref="projects/cs/index.md"):
    errors = []
    return formatter.rewrite_links(text, ref, URLS, errors), errors


class Slugify(unittest.TestCase):
    """Slugs must already be in the form Hugo would urlize them into.

    Each expectation below is a URL the published site actually serves - if
    slugify drifts from Hugo's normalisation, every link to these pages breaks.
    """

    def test_matches_hugo_urlize(self):
        cases = {
            "1-bit MUX": "1-bit-mux",
            "Hazards": "hazards",
            "Regular Expressions (regex)": "regular-expressions-regex",
            "If $n$ is odd, then $n^2$ is odd": "if-n-is-odd-then-n2-is-odd",
            "If $x^2>0$, then $x>0$": "if-x20-then-x0",
        }
        for title, expected in cases.items():
            self.assertEqual(formatter.slugify(title), expected, title)


class ExternalLinks(unittest.TestCase):
    def test_paragraph_with_two_external_links_is_untouched(self):
        # The regression that motivated this rewrite: a greedy regex matched
        # from the first link's "(" to the second link's ")", deleting the
        # text between them and mangling the href.
        line = (
            '> [*"Smashing the Stack for Fun and Profit"*]'
            "(https://phrack.org/issues/49/smashing-the-stack-for-fun-and-profit_md)"
            " is a famous paper published in [Phrack Magazine](https://phrack.org)"
            " detailing how to corrupt the execution stack."
        )
        out, errors = rewrite(line)
        self.assertEqual(out, line)
        self.assertEqual(errors, [])

    def test_schemes_and_absolute_targets_are_untouched(self):
        for dest in (
            "https://phrack.org",
            "http://example.com/a.md",
            "mailto:someone@example.com",
            "//cdn.example.com/x.png",
            "/resume.pdf",
            "#heading",
        ):
            line = "[x]({})".format(dest)
            out, errors = rewrite(line)
            self.assertEqual(out, line, dest)
            self.assertEqual(errors, [], dest)

    def test_external_url_containing_parens_is_untouched(self):
        line = "[wiki](https://en.wikipedia.org/wiki/Stack_(abstract_data_type))"
        out, errors = rewrite(line)
        self.assertEqual(out, line)
        self.assertEqual(errors, [])

    def test_relative_destination_with_balanced_parens(self):
        # Pins paren-depth tracking specifically: unlike the external case
        # above, nothing else here would stop the scan truncating at the first
        # ")" and reporting a bogus unresolvable link.
        urls = {"projects/cs/data/stack_(adt).png": "/docs/cs/stack_(adt).png"}
        errors = []
        out = formatter.rewrite_links(
            "![d](./data/stack_(adt).png)", "projects/cs/index.md", urls, errors
        )
        self.assertEqual(out, "![d](/docs/cs/stack_(adt).png)")
        self.assertEqual(errors, [])

    def test_unterminated_link_is_left_alone(self):
        # Resolvable targets, so a missing ")" is the only thing stopping the
        # rewrite - otherwise the assertion would hold for the wrong reason.
        for line in (
            "[a](<../threat_modelling/docs/index.md",
            "[a](../threat_modelling/docs/index.md",
        ):
            out, errors = rewrite(line)
            self.assertEqual(out, line, line)
            self.assertEqual(errors, [], line)


class RelativeLinks(unittest.TestCase):
    def test_cross_project_link_as_vscode_generates_it(self):
        out, errors = rewrite("[text](../threat_modelling/docs/index.md)")
        self.assertEqual(out, "[text](/docs/threat-modelling/)")
        self.assertEqual(errors, [])

    def test_traversal_out_of_a_nested_section(self):
        out, errors = rewrite(
            "(see [Asymmetric Cryptography](../../docs/index.md))",
            ref="projects/cryptography/cryptography/asymmetric/rsa/docs/index.md",
        )
        self.assertEqual(
            out, "(see [Asymmetric Cryptography](/docs/cryptography/asymmetric-cryptography/))"
        )
        self.assertEqual(errors, [])

    def test_bare_sibling_link(self):
        out, _ = rewrite(
            "* [Elevation of Privelege](eop.md)",
            ref="projects/threat_modelling/docs/identify/index.md",
        )
        self.assertEqual(out, "* [Elevation of Privelege](/docs/threat-modelling/identify/elevation-of-privlege/)")

    def test_fragment_and_query_are_preserved(self):
        out, _ = rewrite("[a](../threat_modelling/docs/index.md#heading)")
        self.assertEqual(out, "[a](/docs/threat-modelling/#heading)")

    def test_percent_encoded_path_is_decoded_before_lookup(self):
        out, errors = rewrite("[a](../threat_modelling/docs/index%2Emd)")
        self.assertEqual(out, "[a](/docs/threat-modelling/)")
        self.assertEqual(errors, [])

    def test_angle_bracket_destination(self):
        out, _ = rewrite("[a](<../threat_modelling/docs/index.md>)")
        self.assertEqual(out, "[a](</docs/threat-modelling/>)")

    def test_destination_with_title(self):
        out, _ = rewrite('[a](../threat_modelling/docs/index.md "Threat Modelling")')
        self.assertEqual(out, '[a](/docs/threat-modelling/ "Threat Modelling")')

    def test_two_links_on_one_line_are_both_rewritten(self):
        out, _ = rewrite(
            "[a](../threat_modelling/docs/index.md) and [b](../fpga/docs/mux.md)"
        )
        self.assertEqual(out, "[a](/docs/threat-modelling/) and [b](/docs/fpga/1-bit-mux/)")


class Assets(unittest.TestCase):
    def test_image_in_a_data_dir_is_flattened_into_the_section(self):
        out, _ = rewrite(
            "![election](data/election.png)",
            ref="projects/threat_modelling/docs/identify/attack_trees/irl.md",
        )
        self.assertEqual(
            out, "![election](/docs/threat-modelling/identify/attack-trees/election.png)"
        )

    def test_pdf_beside_its_page(self):
        out, _ = rewrite("[paper](./bushfire.pdf)", ref="projects/research/bushfire.md")
        self.assertEqual(out, "[paper](/docs/research/bushfire.pdf)")

    def test_html_asset_resolves_to_its_page_url(self):
        # Hugo renders .html in a content dir as a page, so it is reachable at
        # "target/" rather than "target.html".
        out, _ = rewrite(
            "[target.html](./data/target.html)",
            ref="projects/networking/docs/analysis/tools/nmap.md",
        )
        self.assertEqual(out, "[target.html](/docs/networking/network-traffic-analysis/tools/target/)")


class NonLinks(unittest.TestCase):
    def test_parenthesised_prose_is_untouched(self):
        # "(Linux 2.6.17)" reads as name-plus-extension to a naive regex.
        line = "AXIS 210A or 211 Network Camera (Linux 2.6.17) (94%), Synology DSM 5.2-5644"
        out, errors = rewrite(line)
        self.assertEqual(out, line)
        self.assertEqual(errors, [])

    def test_fenced_code_is_untouched(self):
        text = "\n".join(
            [
                "```mermaid",
                'main["`main()`"]',
                "[a](../threat_modelling/docs/index.md)",
                "```",
                "[b](../threat_modelling/docs/index.md)",
            ]
        )
        out, errors = rewrite(text)
        self.assertIn("[a](../threat_modelling/docs/index.md)", out)
        self.assertIn("[b](/docs/threat-modelling/)", out)
        self.assertEqual(errors, [])

    def test_fenced_code_inside_a_blockquote_is_untouched(self):
        # ">" stops a naive fence match, leaving the block scanned as prose.
        text = "> ```\n> [a](../threat_modelling/docs/index.md)\n> ```"
        out, errors = rewrite(text)
        self.assertEqual(out, text)
        self.assertEqual(errors, [])

    def test_links_in_a_blockquote_are_still_rewritten(self):
        out, _ = rewrite("> see [a](../threat_modelling/docs/index.md)")
        self.assertEqual(out, "> see [a](/docs/threat-modelling/)")

    def test_tilde_fence_is_untouched(self):
        text = "~~~\n[a](../threat_modelling/docs/index.md)\n~~~"
        out, _ = rewrite(text)
        self.assertEqual(out, text)

    def test_inline_code_is_untouched(self):
        line = "Use `[a](b.md)` and then [c](../threat_modelling/docs/index.md)."
        out, errors = rewrite(line)
        self.assertEqual(out, "Use `[a](b.md)` and then [c](/docs/threat-modelling/).")
        self.assertEqual(errors, [])


class Unresolvable(unittest.TestCase):
    def test_missing_target_is_reported_not_rewritten(self):
        out, errors = rewrite("[a](./nope.md)")
        self.assertEqual(out, "[a](./nope.md)")
        self.assertEqual(len(errors), 1)
        ref, lineno, dest, target = errors[0]
        self.assertEqual((ref, lineno, dest), ("projects/cs/index.md", 1, "./nope.md"))
        self.assertEqual(target, "projects/cs/nope.md")


class Build(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)

    def _write(self, rel, text):
        path = os.path.join(self.tmp.name, rel)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8") as handle:
            handle.write(text)
        return path

    def _read(self, path):
        with open(path, encoding="utf-8") as handle:
            return handle.read()

    def _page(self, ref, body, url_dir, index=False, front=True, weight=10):
        return {
            "src": self._write("src/" + ref, body),
            "ref": ref,
            "dest": os.path.join(self.tmp.name, "out/content", ref),
            "url_dir": url_dir,
            "weight": weight,
            "index": index,
            "front": front,
        }

    def _manifest(self, pages, assets=()):
        return {
            "roots": [os.path.join(self.tmp.name, "out")],
            "pages": pages,
            "assets": list(assets),
        }

    def test_front_matter_and_link_rewriting(self):
        src = self._write("src/projects/fpga/docs/mux.md", "# 1-bit MUX\n\nBody.\n")
        target = self._write("src/projects/fpga/docs/hazards.md", "# Hazards\n")
        dest = os.path.join(self.tmp.name, "out/content/docs/fpga/mux.md")
        formatter.build(
            self._manifest(
                [
                    {
                        "src": src,
                        "ref": "projects/fpga/docs/mux.md",
                        "dest": dest,
                        "url_dir": "/docs/fpga/",
                        "weight": 20,
                        "index": False,
                        "front": True,
                    },
                    {
                        "src": target,
                        "ref": "projects/fpga/docs/hazards.md",
                        "dest": os.path.join(self.tmp.name, "out/content/docs/fpga/hazards.md"),
                        "url_dir": "/docs/fpga/",
                        "weight": 30,
                        "index": False,
                        "front": True,
                    },
                ]
            )
        )
        written = self._read(dest)
        self.assertIn("title: 1-bit MUX", written)
        self.assertIn("slug: 1-bit-mux", written)
        self.assertIn("weight: 20", written)
        self.assertTrue(written.startswith("---\n"))

    def test_front_false_emits_no_front_matter(self):
        src = self._write("src/README.md", "# tplat\n\nOverview.\n")
        dest = os.path.join(self.tmp.name, "out/content/_index.md")
        formatter.build(
            self._manifest(
                [
                    {
                        "src": src,
                        "ref": "README.md",
                        "dest": dest,
                        "url_dir": "/",
                        "weight": 0,
                        "index": True,
                        "front": False,
                    }
                ]
            )
        )
        self.assertEqual(self._read(dest), "# tplat\n\nOverview.\n")

    def test_assets_are_copied(self):
        page = self._write("src/projects/research/index.md", "# Research\n")
        pdf = self._write("src/projects/research/bushfire.pdf", "%PDF-fake")
        dest = os.path.join(self.tmp.name, "out/content/docs/research/bushfire.pdf")
        formatter.build(
            self._manifest(
                [
                    {
                        "src": page,
                        "ref": "projects/research/index.md",
                        "dest": os.path.join(self.tmp.name, "out/content/docs/research/_index.md"),
                        "url_dir": "/docs/research/",
                        "weight": 1,
                        "index": True,
                        "front": True,
                    }
                ],
                [
                    {
                        "src": pdf,
                        "ref": "projects/research/bushfire.pdf",
                        "dest": dest,
                        "url": "/docs/research/bushfire.pdf",
                    }
                ],
            )
        )
        self.assertEqual(self._read(dest), "%PDF-fake")

    def test_leaf_url_is_derived_from_the_target_pages_own_heading(self):
        # The design claim behind processing the whole tree in one pass: to
        # resolve this link the formatter must first have read mux.md's H1.
        linker = self._page(
            "projects/fpga/docs/hazards.md", "# Hazards\n\n[m](./mux.md)\n", "/docs/fpga/"
        )
        target = self._page("projects/fpga/docs/mux.md", "# 1-bit MUX\n", "/docs/fpga/")
        formatter.build(self._manifest([linker, target]))
        self.assertIn("[m](/docs/fpga/1-bit-mux/)", self._read(linker["dest"]))

    def test_section_index_url_has_no_slug_appended(self):
        linker = self._page(
            "projects/fpga/docs/hazards.md",
            "# Hazards\n\n[up](./index.md)\n",
            "/docs/fpga/",
        )
        section = self._page(
            "projects/fpga/docs/index.md", "# FPGA\n", "/docs/fpga/", index=True
        )
        formatter.build(self._manifest([linker, section]))
        self.assertIn("[up](/docs/fpga/)", self._read(linker["dest"]))

    def test_asset_links_resolve_and_are_percent_encoded(self):
        page = self._page(
            "projects/fpga/docs/index.md",
            # VS Code percent-encodes spaces; a bare space is not a valid
            # CommonMark destination and is left alone by design.
            "# FPGA\n\n![d](./data/my%20diagram.png)\n",
            "/docs/fpga/",
            index=True,
        )
        asset = {
            "src": self._write("src/projects/fpga/docs/data/my diagram.png", "png"),
            "ref": "projects/fpga/docs/data/my diagram.png",
            "dest": os.path.join(self.tmp.name, "out/content/docs/fpga/my diagram.png"),
            "url": "/docs/fpga/my diagram.png",
        }
        formatter.build(self._manifest([page], [asset]))
        self.assertIn("![d](/docs/fpga/my%20diagram.png)", self._read(page["dest"]))

    def test_heading_with_no_usable_slug_fails_the_build(self):
        page = self._page("projects/x/docs/a.md", "# +++\n", "/docs/x/")
        with self.assertRaises(SystemExit):
            formatter.build(self._manifest([page]))

    def test_two_pages_publishing_to_one_url_fail_the_build(self):
        # Distinct files, headings that slugify identically.
        a = self._page("projects/x/docs/a.md", "# Set Up\n", "/docs/x/")
        b = self._page("projects/x/docs/b.md", "# set-up\n", "/docs/x/")
        with self.assertRaises(SystemExit):
            formatter.build(self._manifest([a, b]))

    def test_empty_source_file_fails_the_build(self):
        page = self._page("projects/x/docs/a.md", "", "/docs/x/")
        with self.assertRaises(SystemExit):
            formatter.build(self._manifest([page]))

    def test_unresolvable_link_fails_the_build(self):
        src = self._write("src/projects/cs/index.md", "# CS\n\n[a](./nope.md)\n")
        with self.assertRaises(SystemExit):
            formatter.build(
                self._manifest(
                    [
                        {
                            "src": src,
                            "ref": "projects/cs/index.md",
                            "dest": os.path.join(self.tmp.name, "out/content/docs/cs/_index.md"),
                            "url_dir": "/docs/computer-science/",
                            "weight": 1,
                            "index": True,
                            "front": True,
                        }
                    ]
                )
            )


if __name__ == "__main__":
    unittest.main()
