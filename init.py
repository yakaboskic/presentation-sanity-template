"""Name this project. Run once after "Use this template" or a clone:

    python init.py                       # asks for each answer
    python init.py --yes --title "My talks" --first kickoff --author "Me" --email me@lab.org

A thin shim: it runs `presentation-sanity init --in-place` (see `--help`) with
the version pinned in pyproject.toml, fetched by `uvx` so nothing needs to be
installed first. That command renames the project (pyproject.toml,
package.json, manifest.yaml, README.md), moves presentations/example to your
first presentation, installs the agent skill, and removes this file.

Starting somewhere other than a template copy? Skip this file:
`uvx --from "presentation-sanity @ git+https://github.com/yakaboskic/presentation-sanity.git@vX.Y.Z" presentation-sanity init DIR`.

PRESENTATION_SANITY_FROM overrides where the tool comes from (e.g. a local
checkout, while working on the tool itself).
"""
from __future__ import annotations

import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def pinned_tool() -> str:
    """The presentation-sanity requirement in pyproject.toml, minus extras."""
    text = (ROOT / "pyproject.toml").read_text()
    m = re.search(r'"(presentation-sanity(?:\[[^\]]*\])?\s*@\s*[^"]+)"', text)
    if m is None:
        sys.exit("init.py: no presentation-sanity dependency in pyproject.toml")
    return re.sub(r"\[[^\]]*\]", "", m.group(1), count=1)


def main() -> int:
    args = ["init", "--in-place", str(ROOT), *sys.argv[1:]]
    if shutil.which("uvx"):
        tool = os.environ.get("PRESENTATION_SANITY_FROM") or pinned_tool()
        command = ["uvx", "--from", tool, "presentation-sanity", *args]
    else:
        try:
            import presentation_sanity  # noqa: F401
        except ImportError:
            print(
                "init.py needs uv (https://docs.astral.sh/uv/) to fetch presentation-sanity:\n"
                "  curl -LsSf https://astral.sh/uv/install.sh | sh\n"
                "then run `python init.py` again.",
                file=sys.stderr,
            )
            return 1
        command = [sys.executable, "-m", "presentation_sanity", *args]
    return subprocess.call(command)


if __name__ == "__main__":
    sys.exit(main())
