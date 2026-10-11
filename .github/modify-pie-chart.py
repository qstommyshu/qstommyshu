"""Replace 'other' language label in the generated 3D contribution SVG."""
import re
import sys


def main():
    svg_path = sys.argv[1] if len(sys.argv) > 1 else "profile-3d-contrib/profile-night-green.svg"

    try:
        with open(svg_path, "r") as f:
            svg = f.read()
    except FileNotFoundError:
        print(f"Error: SVG file not found: {svg_path}", file=sys.stderr)
        sys.exit(1)
    except OSError as e:
        print(f"Error reading SVG file: {e}", file=sys.stderr)
        sys.exit(1)

    label = "Languages used in private repos are not displayed"

    modified = False

    # Replace the legend text label: >other< -> >new label<
    new_svg = svg.replace(">other<", f">{label}<")
    if new_svg != svg:
        modified = True
        svg = new_svg

    # Replace the pie slice tooltip: >other NNNN</title> -> >new label NNNN</title>
    new_svg, count = re.subn(r">other (\d+)</title>", rf">{label} \1</title>", svg)
    if count > 0:
        modified = True
        svg = new_svg

    if not modified:
        print("Warning: no 'other' labels found in SVG — nothing to replace", file=sys.stderr)
        sys.exit(1)

    try:
        with open(svg_path, "w") as f:
            f.write(svg)
    except OSError as e:
        print(f"Error writing SVG file: {e}", file=sys.stderr)
        sys.exit(1)

    print("Replaced 'other' labels successfully")


if __name__ == "__main__":
    main()
