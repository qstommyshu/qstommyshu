"""Unit tests for .github/remove-pie-chart.py"""
import os
import subprocess
import sys

import pytest

SCRIPT_PATH = os.path.join(
    os.path.dirname(__file__), os.pardir, ".github", "remove-pie-chart.py"
)


@pytest.fixture
def svg_with_pie(tmp_path):
    """Create a temporary SVG file containing the pie chart group."""
    content = (
        '<svg xmlns="http://www.w3.org/2000/svg">'
        "<g>"
        '<text y="100">Contributions</text>'
        "</g>"
        '<g transform="translate(40, 520)">'
        "<g>"
        '<circle r="50"/>'
        "</g>"
        '<text x="10">Language</text>'
        "</g>"
        "</svg>"
    )
    path = tmp_path / "test.svg"
    path.write_text(content)
    return path


@pytest.fixture
def svg_without_pie(tmp_path):
    """Create a temporary SVG file without the pie chart group."""
    content = (
        '<svg xmlns="http://www.w3.org/2000/svg">'
        "<g>"
        '<text y="100">Contributions</text>'
        "</g>"
        "</svg>"
    )
    path = tmp_path / "test.svg"
    path.write_text(content)
    return path


class TestRemovePieChart:
    """Tests for remove-pie-chart.py script."""

    def test_removes_pie_chart_group(self, svg_with_pie):
        """The script should remove the pie chart <g> element."""
        result = subprocess.run(
            [sys.executable, SCRIPT_PATH, str(svg_with_pie)],
            capture_output=True,
            text=True,
        )
        assert result.returncode == 0
        assert "Pie chart removed successfully" in result.stdout

        modified = svg_with_pie.read_text()
        assert 'translate(40, 520)' not in modified
        assert "<circle" not in modified

    def test_preserves_other_content(self, svg_with_pie):
        """After removing the pie chart, other SVG content should remain."""
        result = subprocess.run(
            [sys.executable, SCRIPT_PATH, str(svg_with_pie)],
            capture_output=True,
            text=True,
        )
        assert result.returncode == 0

        modified = svg_with_pie.read_text()
        assert "Contributions" in modified
        assert "<svg" in modified
        assert "</svg>" in modified

    def test_no_pie_chart_skips(self, svg_without_pie):
        """When no pie chart group exists, the script should skip gracefully."""
        original = svg_without_pie.read_text()
        result = subprocess.run(
            [sys.executable, SCRIPT_PATH, str(svg_without_pie)],
            capture_output=True,
            text=True,
        )
        assert result.returncode == 0
        assert "Pie chart group not found, skipping" in result.stdout

        # File should not be modified
        assert svg_without_pie.read_text() == original

    def test_nested_groups_removed_correctly(self, tmp_path):
        """Deeply nested groups inside the pie chart should all be removed."""
        content = (
            '<svg xmlns="http://www.w3.org/2000/svg">'
            '<g transform="translate(40, 520)">'
            "<g><g><g>"
            '<circle r="10"/>'
            "</g></g></g>"
            "</g>"
            "</svg>"
        )
        path = tmp_path / "nested.svg"
        path.write_text(content)

        result = subprocess.run(
            [sys.executable, SCRIPT_PATH, str(path)],
            capture_output=True,
            text=True,
        )
        assert result.returncode == 0
        assert "Pie chart removed successfully" in result.stdout

        modified = path.read_text()
        assert 'translate(40, 520)' not in modified
        assert "<circle" not in modified
        # Only the outer <svg> tags should remain
        assert modified == '<svg xmlns="http://www.w3.org/2000/svg"></svg>'

    def test_default_path_argument(self, tmp_path, monkeypatch):
        """When no argument is provided, the script uses the default path."""
        default_dir = tmp_path / "profile-3d-contrib"
        default_dir.mkdir()
        svg_path = default_dir / "profile-night-green.svg"
        svg_path.write_text(
            '<svg><g transform="translate(40, 520)"><g></g></g></svg>'
        )

        monkeypatch.chdir(tmp_path)
        result = subprocess.run(
            [sys.executable, SCRIPT_PATH],
            capture_output=True,
            text=True,
            cwd=str(tmp_path),
        )
        assert result.returncode == 0
        assert "Pie chart removed successfully" in result.stdout

        modified = svg_path.read_text()
        assert 'translate(40, 520)' not in modified

    def test_pie_chart_at_end_of_file(self, tmp_path):
        """The pie chart group at the very end of a large SVG is removed."""
        content = (
            '<svg xmlns="http://www.w3.org/2000/svg">'
            '<g transform="translate(0, 0)">'
            '<rect width="100" height="100"/>'
            "</g>"
            '<g transform="translate(40, 520)">'
            '<text x="0">Pie</text>'
            "</g>"
            "</svg>"
        )
        path = tmp_path / "end.svg"
        path.write_text(content)

        result = subprocess.run(
            [sys.executable, SCRIPT_PATH, str(path)],
            capture_output=True,
            text=True,
        )
        assert result.returncode == 0

        modified = path.read_text()
        assert 'translate(40, 520)' not in modified
        assert 'translate(0, 0)' in modified
        assert "Pie" not in modified
