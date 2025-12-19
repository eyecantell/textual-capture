# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**textual-capture** is a Python library for capturing sequenced screenshots of Textual TUI applications. It provides a TOML-based configuration system to automate UI interaction sequences and generate screenshots in SVG and text formats.

## Build System & Package Manager

This project uses **PDM** (Python Development Master) as its package manager and build tool.

### Essential Commands

```bash
# Install dependencies (production only)
pdm install

# Install with test dependencies
pdm install -G test

# Install with lint dependencies
pdm install -G lint

# Install with dev dependencies (includes textual-dev)
pdm install -G dev

# Run tests with coverage
pdm run pytest

# Run a specific test file
pdm run pytest tests/test_specific.py

# Run a specific test
pdm run pytest tests/test_file.py::test_function_name

# Run linting with ruff
pdm run ruff check .

# Run type checking with mypy
pdm run mypy src/textual_capture

# Format code with ruff
pdm run ruff format .
```

## Architecture

### Core Module: `src/textual_capture/capture.py`

The main module provides a universal screenshot capture tool that can work with any Textual application. It operates in two modes:

**1. TOML-based sequence mode (modern approach)**
- Uses a TOML configuration file to define app module, class, window size, and action steps
- Supports multiple action types: `press`, `delay`, `click`, `capture`
- Dynamically imports and instantiates the target Textual app using `run_test()` pilot

**2. Legacy CLI mode**
- Direct command-line arguments for simple one-off captures
- Kept for backward compatibility

### TOML Configuration Structure

When creating sequence files, the expected structure is:
```toml
app_module = "module_name"  # Python module containing the app
app_class = "ClassName"     # Textual App class name
size = [80, 40]             # Terminal size [width, height]

[[step]]
type = "press"
key = "tab enter"           # Space-separated keys

[[step]]
type = "delay"
seconds = 0.5

[[step]]
type = "click"
label = "Button Label"      # Button text (spaces removed for ID)

[[step]]
type = "capture"
output = "snapshot_name"    # Saves .svg and .txt
```

### Dynamic Import Mechanism

The capture tool uses dynamic imports to load arbitrary Textual apps:
- Adds parent directory to `sys.path` for local imports
- Uses `__import__()` with `fromlist` parameter
- Gracefully handles import failures

### Pilot-based Testing

All interactions use Textual's `pilot` API via `app.run_test()`:
- `pilot.press()` for keyboard input
- `pilot.click()` for button interactions (uses `Button#<label>` selector)
- `pilot.pause()` for timing control
- `app.save_screenshot()` for capturing SVG and text output

## Quality Standards

### Test Coverage
- Target: 90% minimum coverage (enforced in CI and `pyproject.toml`)
- Coverage omits: tests, `__pycache__`, `demo*.py` files
- Tests use pytest with async support (`pytest-asyncio`)

### Code Style
- Line length: 120 characters
- Target Python: 3.10+
- Ruff linter with pycodestyle, pyflakes, isort, flake8-bugbear, comprehensions, pyupgrade, simplify
- Exception: E501 (line length) and B008 (function calls in defaults, common in Textual)
- MyPy type checking enabled with strict configuration

## Development Notes

### Python Version Support
Requires Python 3.10+ due to use of `tomllib` (built-in TOML parser introduced in 3.11, but package supports 3.10 via fallback).

### Dependencies
- Primary: `textual>=6.11.0`
- Dev: `textual-dev>=1.8.0` for Textual development tools
- Test: pytest suite with async and coverage plugins

### CI Configuration
There's a discrepancy in `.github/workflows/ci.yml:22` — it references `textual_filelink` instead of `textual_capture` in the coverage path. This should be corrected.
