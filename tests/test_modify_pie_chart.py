"""Unit tests for .github/modify-pie-chart.py"""
import os
import subprocess
import sys
import tempfile

import pytest

SCRIPT_PATH = os.path.join(
    os.path.dirname(__file__), os.pardir, ".github", "modify-pie-chart.py"
)


@pytest.fixture
def svg_file(tmp_path):
    """Create a temporary SVG file with sample content."""
    content = (
        '<svg xmlns="http://www.w3.org/2000/svg">'
        "<g>"
        "<text>other</text>"
        "<title>other 1234</title>"
        "</g>"
        "</svg>"
    )
    path = tmp_path / "test.svg"
    path.write_text(content)
    return path


@pytest.fixture
def svg_file_no_match(tmp_path):
    """Create a temporary SVG file without 'other' labels."""
    content = (
        '<svg xmlns="http://www.w3.org/2000/svg">'
        "<g>"
        "<text>Python</text>"
        "<title>Python 5000</title>"
        "</g>"
        "</svg>"
    )
    path = tmp_path / "test.svg"
    path.write_text(content)
    return path


class TestModifyPieChart:
    """Tests for modify-pie-chart.py script."""

    def test_replaces_legend_text_label(self, svg_file):
        """The script should replace '>other<' with the custom label."""
        result = subprocess.run(
            [sys.executable, SCRIPT_PATH, str(svg_file)],
            capture_output=True,
            text=True,
        )
        assert result.returncode == 0
        assert "Replaced 'other' labels successfully" in result.stdout

        modified = svg_file.read_text()
        expected_label = "Languages used in private repos are not displayed"
        assert f">{expected_label}<" in modified
        assert ">other<" not in modified

    def test_replaces_pie_slice_tooltip(self, svg_file):
        """The script should replace '>other NNNN</title>' with the custom label."""
        result = subprocess.run(
            [sys.executable, SCRIPT_PATH, str(svg_file)],
            capture_output=True,
            text=True,
        )
        assert result.returncode == 0

        modified = svg_file.read_text()
        expected_label = "Languages used in private repos are not displayed"
        assert f">{expected_label} 1234</title>" in modified
        assert ">other 1234</title>" not in modified

    def test_no_match_leaves_file_unchanged(self, svg_file_no_match):
        """When 'other' is not present, the file content should stay the same."""
        original = svg_file_no_match.read_text()
        result = subprocess.run(
            [sys.executable, SCRIPT_PATH, str(svg_file_no_match)],
            capture_output=True,
            text=True,
        )
        assert result.returncode == 0

        modified = svg_file_no_match.read_text()
        assert modified == original

    def test_multiple_other_labels(self, tmp_path):
        """The script should replace all occurrences of 'other' labels."""
        content = (
            '<svg xmlns="http://www.w3.org/2000/svg">'
            "<g>"
            "<text>other</text>"
            "<text>other</text>"
            "<title>other 100</title>"
            "<title>other 200</title>"
            "</g>"
            "</svg>"
        )
        path = tmp_path / "multi.svg"
        path.write_text(content)

        result = subprocess.run(
            [sys.executable, SCRIPT_PATH, str(path)],
            capture_output=True,
            text=True,
        )
        assert result.returncode == 0

        modified = path.read_text()
        expected_label = "Languages used in private repos are not displayed"
        assert modified.count(f">{expected_label}<") == 2
        assert ">other<" not in modified
        assert ">other 100</title>" not in modified
        assert ">other 200</title>" not in modified

    def test_default_path_argument(self, tmp_path, monkeypatch):
        """When no argument is provided, the script uses the default path."""
        # Create the expected default file relative to cwd
        default_dir = tmp_path / "profile-3d-contrib"
        default_dir.mkdir()
        svg_path = default_dir / "profile-night-green.svg"
        svg_path.write_text("<svg><text>other</text></svg>")

        monkeypatch.chdir(tmp_path)
        result = subprocess.run(
            [sys.executable, SCRIPT_PATH],
            capture_output=True,
            text=True,
            cwd=str(tmp_path),
        )
        assert result.returncode == 0

        modified = svg_path.read_text()
        expected_label = "Languages used in private repos are not displayed"
        assert f">{expected_label}<" in modified
