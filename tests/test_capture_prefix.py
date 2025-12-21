"""Tests for capture_prefix configuration option."""

from pathlib import Path
from unittest.mock import patch

import pytest

from textual_capture.capture import capture, main, validate_config


class TestCapturePrefix:
    """Tests for capture_prefix configuration."""

    async def test_capture_prefix_default(self, tmp_path: Path, temp_dir: Path):
        """Default prefix is 'capture'."""
        toml_content = """
app_module = "tests.conftest"
app_class = "SimpleTestApp"

[[step]]
type = "capture"
"""
        toml_file = tmp_path / "config.toml"
        toml_file.write_text(toml_content)

        await capture(str(toml_file))

        assert (temp_dir / "capture_001.svg").exists()
        assert (temp_dir / "capture_001.txt").exists()
        assert (temp_dir / "capture_001_tooltips.txt").exists()

    async def test_capture_prefix_custom(self, tmp_path: Path, temp_dir: Path):
        """Custom prefix is used for auto-sequenced captures."""
        toml_content = """
app_module = "tests.conftest"
app_class = "SimpleTestApp"
capture_prefix = "myapp"

[[step]]
type = "capture"

[[step]]
type = "capture"
"""
        toml_file = tmp_path / "config.toml"
        toml_file.write_text(toml_content)

        await capture(str(toml_file))

        assert (temp_dir / "myapp_001.svg").exists()
        assert (temp_dir / "myapp_001.txt").exists()
        assert (temp_dir / "myapp_001_tooltips.txt").exists()
        assert (temp_dir / "myapp_002.svg").exists()
        assert (temp_dir / "myapp_002.txt").exists()
        assert (temp_dir / "myapp_002_tooltips.txt").exists()

    async def test_capture_prefix_multiple_captures(self, tmp_path: Path, temp_dir: Path):
        """Multiple auto-sequenced captures use prefix correctly."""
        toml_content = """
app_module = "tests.conftest"
app_class = "SimpleTestApp"
capture_prefix = "sequence"

[[step]]
type = "capture"

[[step]]
type = "press"
keys = ["tab"]

[[step]]
type = "capture"

[[step]]
type = "capture"
"""
        toml_file = tmp_path / "config.toml"
        toml_file.write_text(toml_content)

        await capture(str(toml_file))

        assert (temp_dir / "sequence_001.svg").exists()
        assert (temp_dir / "sequence_002.svg").exists()
        assert (temp_dir / "sequence_003.svg").exists()

    async def test_capture_prefix_with_explicit_output(self, tmp_path: Path, temp_dir: Path):
        """Explicit output names ignore capture_prefix."""
        toml_content = """
app_module = "tests.conftest"
app_class = "SimpleTestApp"
capture_prefix = "auto"

[[step]]
type = "capture"
output = "explicit_name"

[[step]]
type = "capture"
# Should use prefix for auto-sequence
"""
        toml_file = tmp_path / "config.toml"
        toml_file.write_text(toml_content)

        await capture(str(toml_file))

        # Explicit name ignores prefix
        assert (temp_dir / "explicit_name.svg").exists()
        assert (temp_dir / "explicit_name.txt").exists()

        # Auto-sequence uses prefix and continues counting
        assert (temp_dir / "auto_001.svg").exists()
        assert (temp_dir / "auto_001.txt").exists()

    async def test_capture_prefix_with_output_dir(self, tmp_path: Path):
        """capture_prefix works with output_dir."""
        output_dir = tmp_path / "screenshots"
        toml_content = f"""
app_module = "tests.conftest"
app_class = "SimpleTestApp"
output_dir = "{output_dir}"
capture_prefix = "test"

[[step]]
type = "capture"
"""
        toml_file = tmp_path / "config.toml"
        toml_file.write_text(toml_content)

        await capture(str(toml_file))

        assert (output_dir / "test_001.svg").exists()
        assert (output_dir / "test_001.txt").exists()
        assert (output_dir / "test_001_tooltips.txt").exists()

    def test_validate_capture_prefix_must_be_string(self):
        """capture_prefix must be a string."""
        config = {
            "app_module": "test",
            "app_class": "Test",
            "capture_prefix": 123,  # Not a string
        }

        with pytest.raises(ValueError, match="'capture_prefix' must be a string"):
            validate_config(config)

    def test_validate_capture_prefix_cannot_be_empty(self):
        """capture_prefix cannot be empty string."""
        config = {
            "app_module": "test",
            "app_class": "Test",
            "capture_prefix": "",
        }

        with pytest.raises(ValueError, match="'capture_prefix' cannot be empty"):
            validate_config(config)

    def test_validate_capture_prefix_no_forward_slash(self):
        """capture_prefix cannot contain forward slash."""
        config = {
            "app_module": "test",
            "app_class": "Test",
            "capture_prefix": "my/prefix",
        }

        with pytest.raises(ValueError, match="invalid characters"):
            validate_config(config)

    def test_validate_capture_prefix_no_backslash(self):
        """capture_prefix cannot contain backslash."""
        config = {
            "app_module": "test",
            "app_class": "Test",
            "capture_prefix": "my\\prefix",
        }

        with pytest.raises(ValueError, match="invalid characters"):
            validate_config(config)

    def test_validate_capture_prefix_no_colon(self):
        """capture_prefix cannot contain colon (Windows unsafe)."""
        config = {
            "app_module": "test",
            "app_class": "Test",
            "capture_prefix": "my:prefix",
        }

        with pytest.raises(ValueError, match="invalid characters"):
            validate_config(config)

    def test_validate_capture_prefix_no_asterisk(self):
        """capture_prefix cannot contain asterisk."""
        config = {
            "app_module": "test",
            "app_class": "Test",
            "capture_prefix": "my*prefix",
        }

        with pytest.raises(ValueError, match="invalid characters"):
            validate_config(config)

    def test_validate_capture_prefix_no_question_mark(self):
        """capture_prefix cannot contain question mark."""
        config = {
            "app_module": "test",
            "app_class": "Test",
            "capture_prefix": "my?prefix",
        }

        with pytest.raises(ValueError, match="invalid characters"):
            validate_config(config)

    def test_validate_capture_prefix_allows_underscore(self):
        """capture_prefix can contain underscore."""
        config = {
            "app_module": "test",
            "app_class": "Test",
            "capture_prefix": "my_prefix",
        }

        # Should not raise
        validate_config(config)

    def test_validate_capture_prefix_allows_dash(self):
        """capture_prefix can contain dash."""
        config = {
            "app_module": "test",
            "app_class": "Test",
            "capture_prefix": "my-prefix",
        }

        # Should not raise
        validate_config(config)

    def test_dry_run_shows_capture_prefix_default(self, tmp_path: Path, capsys):
        """Dry-run displays default capture_prefix."""
        toml_content = """
app_module = "tests.conftest"
app_class = "SimpleTestApp"

[[step]]
type = "capture"
"""
        toml_file = tmp_path / "config.toml"
        toml_file.write_text(toml_content)

        with patch("sys.argv", ["textual-capture", str(toml_file), "--dry-run"]):
            with pytest.raises(SystemExit) as exc_info:
                main()

            assert exc_info.value.code == 0

            captured = capsys.readouterr()
            assert "Capture Prefix: capture" in captured.out
            assert 'output="capture_001"' in captured.out

    def test_dry_run_shows_capture_prefix_custom(self, tmp_path: Path, capsys):
        """Dry-run displays custom capture_prefix."""
        toml_content = """
app_module = "tests.conftest"
app_class = "SimpleTestApp"
capture_prefix = "my_sequence"

[[step]]
type = "capture"

[[step]]
type = "capture"
"""
        toml_file = tmp_path / "config.toml"
        toml_file.write_text(toml_content)

        with patch("sys.argv", ["textual-capture", str(toml_file), "--dry-run"]):
            with pytest.raises(SystemExit) as exc_info:
                main()

            assert exc_info.value.code == 0

            captured = capsys.readouterr()
            assert "Capture Prefix: my_sequence" in captured.out
            assert 'output="my_sequence_001"' in captured.out
            assert 'output="my_sequence_002"' in captured.out
