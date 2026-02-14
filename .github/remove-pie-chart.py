"""Remove the pie language chart from the generated 3D contribution SVG."""
import re
import sys

svg_path = sys.argv[1] if len(sys.argv) > 1 else "profile-3d-contrib/profile-night-green.svg"

with open(svg_path, "r") as f:
    svg = f.read()

# Remove the pie chart group: <g transform="translate(40, 520)">
# where y = height(850) - pieHeight(260) - 70 = 520
idx = svg.find('<g transform="translate(40, 520)">')
if idx != -1:
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
    with open(svg_path, "w") as f:
        f.write(svg)
    print("Pie chart removed successfully")
else:
    print("Pie chart group not found, skipping")
