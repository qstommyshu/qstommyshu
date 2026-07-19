"""Shared utilities for SVG post-processing scripts."""

import sys

DEFAULT_SVG_PATH = "profile-3d-contrib/profile-night-green.svg"


def get_svg_path() -> str:
    """Return the SVG file path from CLI args or the default."""
    return sys.argv[1] if len(sys.argv) > 1 else DEFAULT_SVG_PATH


def load_svg(path: str) -> str:
    """Read and return the contents of an SVG file."""
    with open(path, "r") as f:
        return f.read()


def save_svg(path: str, content: str) -> None:
    """Write content back to an SVG file."""
    with open(path, "w") as f:
        f.write(content)


def remove_svg_group(svg: str, transform: str) -> str | None:
    """Remove the first <g> element matching the given transform attribute.

    Returns the modified SVG string, or None if the group was not found.
    """
    target = f'<g transform="{transform}">'
    idx = svg.find(target)
    if idx == -1:
        return None

    depth = 0
    i = idx
    while i < len(svg):
        if svg[i : i + 2] == "<g":
            depth += 1
        elif svg[i : i + 4] == "</g>":
            depth -= 1
            if depth == 0:
                return svg[:idx] + svg[i + 4 :]
        i += 1
    return None
