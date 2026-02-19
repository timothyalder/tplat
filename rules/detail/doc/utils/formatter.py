import sys
import os

def transform(src, dest):
    with open(src, 'r') as f:
        lines = f.readlines()

    if not lines:
        print(f"ERROR: {src} is empty.")
        sys.exit(1)

    if not lines[0].strip().startswith("# "):
        print(f"ERROR: {src} must begin with a H1 title (e.g., '# My Title').")
        print(f"Found: '{lines[0].strip()}'")
        sys.exit(1)
        
    title = lines[0].strip().replace("# ", "")
    
    front_matter = [
        "---",
        f"title: {title}",
        "type: docs",
        "---",
        "",
    ]
    body = [line.rstrip() for line in lines]
    output = front_matter + body

    os.makedirs(os.path.dirname(dest), exist_ok=True)
    with open(dest, 'w') as f:
        f.write("\n".join(output))

if __name__ == "__main__":
    if len(sys.argv) < 3:
        sys.exit(1)
    transform(sys.argv[1], sys.argv[2])