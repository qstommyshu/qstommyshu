"""Replace 'other' language label in the generated 3D contribution SVG."""

import re

from svg_utils import get_svg_path, load_svg, save_svg

svg_path = get_svg_path()
svg = load_svg(svg_path)

label = "Languages used in private repos are not displayed"

# Replace the legend text label: >other< -> >new label<
svg = svg.replace(">other<", f">{label}<")

# Replace the pie slice tooltip: >other NNNN</title> -> >new label NNNN</title>
svg = re.sub(r">other (\d+)</title>", rf">{label} \1</title>", svg)

save_svg(svg_path, svg)

print("Replaced 'other' labels successfully")
