"""Bootstrap a fresh deck cloned from presentation-sanity-template.

Prompts for name, title, author, description; rewrites pyproject.toml,
package.json, manifest.yaml, README.md; refreshes uv.lock; offers to
remove itself when done. Run once on a fresh clone:

    python init.py
"""
import re
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).parent
SELF = Path(__file__)

PYPROJECT = ROOT / "pyproject.toml"
PACKAGE_JSON = ROOT / "package.json"
MANIFEST = ROOT / "manifest.yaml"
README = ROOT / "README.md"

TEMPLATE_NAME = "presentation-sanity-template"


def already_initialized() -> bool:
    return TEMPLATE_NAME not in PYPROJECT.read_text()


def ask(prompt: str, default: str | None = None) -> str:
    suffix = f" [{default}]" if default else ""
    while True:
        answer = input(f"{prompt}{suffix}: ").strip()
        if answer:
            return answer
        if default is not None:
            return default
        print("  (required)")


def confirm(prompt: str, default: bool = True) -> bool:
    suffix = "[Y/n]" if default else "[y/N]"
    answer = input(f"{prompt} {suffix} ").strip().lower()
    if not answer:
        return default
    return answer in ("y", "yes")


def render_readme(slug: str, description: str) -> str:
    return f"""# {slug}

{description}

Built on [presentation-sanity](https://github.com/yakaboskic/presentation-sanity).
See [presentation-sanity-template](https://github.com/yakaboskic/presentation-sanity-template)
for documentation on layouts, manim scenes, the manifest schema, and the
provenance panel.

## Develop

```bash
uv sync                                 # Python deps (presentation-sanity[manim])
npm install                             # Slidev deps
uv run presentation-sanity dev          # hot-reload at localhost:3030
uv run presentation-sanity build        # static bundle → dist/
uv run presentation-sanity preview      # serve dist/ at localhost:8000
uv run presentation-sanity export pdf
```

For manim, you'll also need `ffmpeg`, `cairo`, `pango`, and a LaTeX install.
"""


def main() -> None:
    if already_initialized():
        print("This deck looks already initialized — no template placeholders found.")
        print("Delete init.py if you haven't, or restore the template files first.")
        sys.exit(0)

    print("Setting up a new deck. Defaults shown in [brackets].\n")
    slug = ask("Project slug (kebab-case)", default=ROOT.name)
    title = ask("Deck title")
    author = ask("Author name")
    email = ask("Author email")
    description = ask("Short description", default=f"Talk: {title}")

    pyproject = PYPROJECT.read_text()
    pyproject = pyproject.replace(
        f'name = "{TEMPLATE_NAME}"', f'name = "{slug}"', 1
    )
    pyproject = re.sub(
        r'^description = "[^"]*"',
        f'description = "{description}"',
        pyproject,
        count=1,
        flags=re.MULTILINE,
    )
    PYPROJECT.write_text(pyproject)

    package = PACKAGE_JSON.read_text()
    package = package.replace(
        f'"name": "{TEMPLATE_NAME}"', f'"name": "{slug}"', 1
    )
    PACKAGE_JSON.write_text(package)

    manifest = MANIFEST.read_text()
    manifest = re.sub(r'title:\s*"[^"]*"', f'title: "{title}"', manifest, count=1)
    manifest = re.sub(r'name:\s*"[^"]*"', f'name: "{author}"', manifest, count=1)
    manifest = re.sub(r'email:\s*"[^"]*"', f'email: "{email}"', manifest, count=1)
    MANIFEST.write_text(manifest)

    README.write_text(render_readme(slug, description))

    print(f"\nRewrote pyproject.toml, package.json, manifest.yaml, README.md.")

    if shutil.which("uv"):
        print("Refreshing uv.lock...")
        result = subprocess.run(["uv", "lock"], cwd=ROOT)
        if result.returncode != 0:
            print("uv lock failed — run it yourself when ready.")
    else:
        print("uv not found on PATH — run `uv lock` (or `uv sync`) once installed.")

    print()
    print(f"Initialized {slug}.")
    print()
    print("Next steps:")
    print("  uv sync           # install Python deps")
    print("  npm install       # install Slidev deps")
    print("  uv run presentation-sanity dev")
    print()

    if confirm("Remove init.py?"):
        SELF.unlink()
        print("Removed init.py.")
    else:
        print("Kept init.py — delete when ready.")


if __name__ == "__main__":
    main()
