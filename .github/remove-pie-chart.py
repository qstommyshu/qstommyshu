"""Remove the pie language chart from the generated 3D contribution SVG."""

from svg_utils import get_svg_path, load_svg, remove_svg_group, save_svg

svg_path = get_svg_path()
svg = load_svg(svg_path)

# Remove the pie chart group: <g transform="translate(40, 520)">
# where y = height(850) - pieHeight(260) - 70 = 520
result = remove_svg_group(svg, "translate(40, 520)")
if result is not None:
    save_svg(svg_path, result)
    print("Pie chart removed successfully")
else:
    print("Pie chart group not found, skipping")
