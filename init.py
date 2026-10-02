"""Bootstrap a fresh project cloned from presentation-sanity-template.

Prompts for the project (name, title, authors, description) and its first
presentation (folder name, deck title); rewrites pyproject.toml, package.json,
manifest.yaml and README.md, renames presentations/example to your first
presentation, refreshes uv.lock, and offers to remove itself. Run once on a
fresh clone:

    python init.py
"""
from __future__ import annotations

import json
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
PRESENTATIONS = ROOT / "presentations"
EXAMPLE = PRESENTATIONS / "example"

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


def set_headmatter_title(path: Path, title: str) -> None:
    """Set `title:` in a deck's first frontmatter block, keeping comments."""
    text = path.read_text()
    m = re.match(r"(\s*---\n)(.*?)(\n---)", text, re.S)
    if m is None:
        return
    line = f"title: {json.dumps(title, ensure_ascii=False)}"
    body = re.sub(r"^title:.*$", lambda _: line, m.group(2), count=1, flags=re.M)
    path.write_text(text[: m.start(2)] + body + text[m.end(2):])


def render_readme(slug: str, description: str, first: str) -> str:
    return f"""# {slug}

{description}

Built on [presentation-sanity](https://github.com/yakaboskic/presentation-sanity).
See [presentation-sanity-template](https://github.com/yakaboskic/presentation-sanity-template)
for documentation on presentations and versions, the manifest schema, layouts,
manim scenes and the provenance panel.

Every folder under `presentations/` with a `slides.md` (Slidev) and/or a
`blog.md` (VitePress) is a presentation. They all share `manifest.yaml`
(variables, scenes, figures, bibliography), `public/` and the `shared/`
components and layouts.

## Develop

```bash
uv sync                                       # Python deps (presentation-sanity)
npm install                                   # Slidev + VitePress (+ links shared/)
uv run presentation-sanity list               # presentations in this project
uv run presentation-sanity dev {first}         # Slidev hot-reload at :3030
uv run presentation-sanity new {first}-v2 --from {first}   # fork a new version
uv run presentation-sanity build              # everything → site/ (+ site/index.html)
uv run presentation-sanity preview            # serve site/ at :8000
```

For manim, you'll also need `ffmpeg`, `cairo`, `pango`, and a LaTeX install.
"""


def main() -> None:
    if already_initialized():
        print("This project looks already initialized — no template placeholders found.")
        print("Delete init.py if you haven't, or restore the template files first.")
        sys.exit(0)

    print("Setting up a new project. Defaults shown in [brackets].\n")
    slug = ask("Project slug (kebab-case)", default=ROOT.name)
    title = ask("Project title (e.g. the program or grant name)")
    author = ask("Author name")
    email = ask("Author email")
    description = ask("Short description", default=f"Presentations about {title}")
    first = ask("First presentation folder (e.g. kickoff, or kickoff/v1)", default="kickoff")
    deck_title = ask("First presentation's title", default=title)

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
    manifest = re.sub(
        r'description:\s*"[^"]*"', f'description: "{description}"', manifest, count=1
    )
    manifest = re.sub(r'name:\s*"[^"]*"', f'name: "{author}"', manifest, count=1)
    manifest = re.sub(r'email:\s*"[^"]*"', f'email: "{email}"', manifest, count=1)
    MANIFEST.write_text(manifest)

    first = first.strip().strip("/")
    target = PRESENTATIONS / first
    if EXAMPLE.is_dir() and target != EXAMPLE:
        target.parent.mkdir(parents=True, exist_ok=True)
        EXAMPLE.rename(target)
    if (target / "slides.md").is_file():
        set_headmatter_title(target / "slides.md", deck_title)

    README.write_text(render_readme(slug, description, first))

    print(
        f"\nRewrote pyproject.toml, package.json, manifest.yaml, README.md; "
        f"first presentation is presentations/{first}/."
    )

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
    print("  npm install       # install Slidev + VitePress, link shared/")
    print(f"  uv run presentation-sanity dev {first}")
    print()

    if confirm("Remove init.py?"):
        SELF.unlink()
        print("Removed init.py.")
    else:
        print("Kept init.py — delete when ready.")


if __name__ == "__main__":
    main()
