import argparse
import sys
import os
import re
import shutil


def transform(src: str, *args, **kwargs):
    (
        transform_file(src, *args, **kwargs)
        if os.path.isfile(src)
        else transform_dir(src, *args, **kwargs)
    )


def transform_dir(src: str, dest: str, weight: int = 10):
    # Only ignore the _index.md file inside src root
    def ignore_root_index(dirpath, names):
        if os.path.abspath(dirpath) == os.path.abspath(src):
            return ["_index.md"] if "_index.md" in names else []
        return []
    shutil.copytree(src, dest, ignore=ignore_root_index)

    src_index = os.path.join(src, "_index.md")
    dest_index = os.path.join(dest, "_index.md")

    with open(src_index, "r") as f_in:
        lines = f_in.readlines()

    with open(dest_index, "w") as f_out:
        title = lines[0].strip().replace("# ", "")
        for line in lines:
            if line.startswith("weight: "):
                f_out.write(f"weight: {weight}\nslug: {title.lower().replace(' ', '')}\n") # Doesn't work for _index.md https://github.com/gohugoio/hugo/issues/7124
            else:
                f_out.write(line)


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
        transform(args.src, args.dest, args.weight)
    except Exception as e:
        print(f"Error transforming {args.src}: {e}")
        sys.exit(1)
