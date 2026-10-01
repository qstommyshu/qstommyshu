"""Remove the pie language chart from the generated 3D contribution SVG."""
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

    # Remove the pie chart group: <g transform="translate(40, 520)">
    # where y = height(850) - pieHeight(260) - 70 = 520
    idx = svg.find('<g transform="translate(40, 520)">')
    if idx == -1:
        print("Pie chart group not found, skipping")
        return

    depth = 0
    i = idx
    while i < len(svg):
        if svg[i:i+2] == "<g":
            depth += 1
        elif svg[i:i+4] == "</g>":
            depth -= 1
            if depth == 0:
                svg = svg[:idx] + svg[i+4:]
                break
        i += 1
    else:
        print("Error: malformed SVG — no matching </g> found for pie chart group", file=sys.stderr)
        sys.exit(1)

    try:
        with open(svg_path, "w") as f:
            f.write(svg)
    except OSError as e:
        print(f"Error writing SVG file: {e}", file=sys.stderr)
        sys.exit(1)

    print("Pie chart removed successfully")


if __name__ == "__main__":
    main()
