"""Replace 'other' language label in the generated 3D contribution SVG."""
import re
import sys

svg_path = sys.argv[1] if len(sys.argv) > 1 else "profile-3d-contrib/profile-night-green.svg"

with open(svg_path, "r") as f:
    svg = f.read()

label = "languages used in primary repo are not displayed."

# Replace the legend text label: >other< -> >new label<
svg = svg.replace(">other<", f">{label}<")

# Replace the pie slice tooltip: >other NNNN</title> -> >new label NNNN</title>
svg = re.sub(r">other (\d+)</title>", rf">{label} \1</title>", svg)

with open(svg_path, "w") as f:
    f.write(svg)

print("Replaced 'other' labels successfully")
