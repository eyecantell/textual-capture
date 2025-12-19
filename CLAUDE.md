# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**textual-capture** is a Python library for capturing sequenced screenshots of Textual TUI applications. It provides a TOML-based configuration system to automate UI interaction sequences and generate screenshots in SVG and text formats.

**Primary Use Case**: Enable LLMs to review and test Textual TUIs by capturing screenshots at different states.

## Build System & Package Manager

This project uses **PDM** (Python Development Master) as its package manager and build tool.

### Essential Commands

```bash
# Install dependencies (production only)
pdm install

# Install with test dependencies
pdm install --dev

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

The main module provides a universal screenshot capture tool that can work with any Textual application via TOML-based configuration files.

**Key Features**:
- Uses a TOML configuration file to define app module, class, window size, and action steps
- Supports multiple action types: `press`, `delay`, `click`, `capture`
- Dynamically imports and instantiates the target Textual app using `run_test()` pilot
- Auto-sequences screenshots when output name is omitted
- Python logging with `--verbose` and `--quiet` flags

### TOML Configuration Structure

Current API (as of v0.1.0):
```toml
app_module = "module_name"         # Required: Python module containing the app
app_class = "ClassName"            # Required: Textual App class name
screen_width = 80                  # Optional: Terminal width (default: 80)
screen_height = 40                 # Optional: Terminal height (default: 40)
initial_delay = 1.0                # Optional: Wait before first action (default: 1.0)
scroll_to_top = true               # Optional: Press "home" at start (default: true)
module_path = "path/to/module"     # Optional: Add to sys.path for imports

[[step]]
type = "press"
key = "tab,enter"                  # Comma-separated keys

[[step]]
type = "delay"
seconds = 0.5

[[step]]
type = "click"
label = "Button Label"             # Button text (spaces removed for ID)

[[step]]
type = "capture"
output = "snapshot_name"           # Optional: custom name (auto-generates if omitted)
```

**Auto-sequencing**: Omit `output` field in capture actions to auto-generate `capture_001.svg`, `capture_002.svg`, etc.

### Dynamic Import Mechanism

The capture tool uses dynamic imports to load arbitrary Textual apps:
- Uses `module_path` config option to add to `sys.path` for local imports
- Uses `__import__()` with `fromlist` parameter
- Gracefully handles import failures with clear error messages

### Pilot-based Testing

All interactions use Textual's `pilot` API via `app.run_test()`:
- `pilot.press()` for keyboard input
- `pilot.click()` for button interactions (uses `Button#<label>` selector)
- `pilot.pause()` for timing control
- `app.save_screenshot()` for capturing SVG and text output

## Using textual-capture in Claude Code

### When to Use This Tool

Claude Code should **proactively** use `textual-capture` when:

1. **After making TUI changes**: Automatically capture screenshots to verify visual changes
   - Example: "I updated the button layout. Let me capture screenshots to verify..."
   - Create a TOML config, run capture, read .txt output, report findings

2. **When user asks to review UI**: Generate captures to analyze layout/appearance
   - User: "Does my dialog look right?"
   - Claude: Creates TOML, runs capture, reviews output, provides feedback

3. **During TUI development**: Test interaction sequences work as expected
   - Verify keyboard navigation flows
   - Check that click targets are accessible
   - Validate multi-step workflows

### How to Use It

**Step 1: Create a TOML configuration**
```python
# Use Write tool to create a .toml file with the capture sequence
# See examples/llm_review.toml for a template
```

**Step 2: Run textual-capture**
```bash
pdm run textual-capture your_config.toml --verbose
```

**Step 3: Analyze output**
- Read the .txt files (plain text representation of UI)
- Optionally mention .svg files exist for user to view
- Report findings to user

### Template for Quick Reviews

When the user has a Textual app in development, create this config:

```toml
app_module = "user_app_module"    # Get from user's project structure
app_class = "UserAppClass"        # Main App class
module_path = "."                 # Usually current directory

# Capture initial state
[[step]]
type = "capture"
output = "initial_state"

# Navigate to area of interest (adapt as needed)
[[step]]
type = "press"
key = "tab,tab,enter"

[[step]]
type = "capture"
output = "after_interaction"
```

### Best Practices

1. **Use module_path**: Always set `module_path = "."` or appropriate path so imports work
2. **Auto-sequence for exploration**: Omit `output` field to auto-generate capture_001, capture_002, etc.
3. **Named captures for specific states**: Use `output = "descriptive_name"` for key moments
4. **Read .txt files**: The text representation is perfect for LLM analysis
5. **Verbose mode for debugging**: Use `--verbose` to see what's happening

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
Requires Python 3.10+ with conditional TOML parser import:
- Python 3.11+: Uses built-in `tomllib`
- Python 3.10: Falls back to `tomli` package

### Dependencies
- Primary: `textual>=6.11.0`
- Python 3.10: `tomli>=2.0.0` (conditional)
- Dev: `textual-dev>=1.8.0` for Textual development tools
- Test: pytest suite with async and coverage plugins
