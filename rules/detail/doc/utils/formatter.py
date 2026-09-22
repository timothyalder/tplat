import argparse
import sys
import re


def transform_file(src: str, dest: str, weight: int = 10):
    with open(src, "r") as f:
        lines = f.readlines()

    if not lines:
        print(f"ERROR: {src} is empty.")
        sys.exit(1)

    title = lines[0].strip().replace("# ", "")

    front_matter = [
        "---",
        f"title: {title}",
        "type: docs",
        f"weight: {weight}",
        f"slug: {title.lower().replace(' ', '-')}",
        "bookCollapseSection: true",
        "---",
        "",
    ]

    body_text = "\n".join([line.rstrip() for line in lines])
    body_text = re.sub(
        r"\((?:.*?/)?([^/)]+?)(\.md|(\.[a-zA-Z0-9]+))\)",
        lambda m: f"(../{m.group(1)}{'' if m.group(2)=='.md' else m.group(2)})",
        body_text,
    )

    with open(dest, "w") as f:
        f.write("\n".join(front_matter) + body_text)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Hugo Doc Formatter")
    parser.add_argument("src", help="Source markdown file")
    parser.add_argument("dest", help="Destination path for index.md")
    parser.add_argument(
        "--weight",
        type=int,
        default=10,
        help="Menu weight for the page (defaults to 10)",
    )

    args = parser.parse_args()

    try:
        transform_file(args.src, args.dest, args.weight)
    except Exception as e:
        print(f"Error transforming {args.src}: {e}")
        sys.exit(1)
