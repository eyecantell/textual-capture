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

Current API (as of v0.2.0):
```toml
# Required
app_module = "module_name"         # Python module containing the app
app_class = "ClassName"            # Textual App class name

# Output configuration
output_dir = "./screenshots"       # Where to save files (default: ".")
formats = ["svg", "txt"]           # Formats to generate (default: both)

# Tooltip capture (enabled by default)
capture_tooltips = true            # Auto-capture tooltips with screenshots
widget_selector = "*"             # CSS selector for widgets (default: all)
tooltip_include_empty = false      # Include widgets without tooltips

# Screen and timing
screen_width = 80                  # Terminal width (default: 80)
screen_height = 40                 # Terminal height (default: 40)
initial_delay = 1.0                # Wait before first action (default: 1.0)
scroll_to_top = true               # Press "home" at start (default: true)
module_path = "path/to/module"     # Add to sys.path for imports (optional)

# Action steps
[[step]]
type = "press"
keys = ["tab", "enter"]            # List syntax (preferred)
pause_between = 0.2                  # Seconds between keys (optional)

[[step]]
type = "delay"
seconds = 0.5

[[step]]
type = "click"
label = "Button Label"             # Button text (spaces removed for ID)

[[step]]
type = "capture"
output = "snapshot_name"           # Optional: custom name (auto-generates if omitted)
formats = ["svg", "txt"]           # Optional: override global formats
capture_tooltips = true            # Optional: override global tooltip setting
widget_selector = "Button"        # Optional: filter widgets for this capture
```

**Key Features**:
- **Auto-sequencing**: Omit `output` field to auto-generate `capture_001`, `capture_002`, etc.
- **Tooltips**: Each capture creates a `{output}_tooltips.txt` file with widget tooltips
- **Selective formats**: Use `formats = ["svg"]` or `["txt"]` to generate only what you need
- **Tooltip-only captures**: Use `formats = []` with `capture_tooltips = true` for fast metadata extraction

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
   - Use **Example #1 (Quick UI Review)** or **Example #4 (Documentation Screenshots)**

2. **When user asks to review UI**: Generate captures to analyze layout/appearance
   - User: "Does my dialog look right?"
   - Use **Example #1 (Quick UI Review)**

3. **When user asks about tooltips or accessibility**:
   - User: "Check if all buttons have tooltips"
   - Use **Example #2 (Tooltip Accessibility Audit)**

4. **During TUI development**: Test interaction sequences work as expected
   - Verify keyboard navigation flows → **Example #3 (Keyboard Navigation Testing)**
   - Check button clicks work → **Example #6 (Button Click Verification)**
   - Explore app features → **Example #5 (Full App Exploration)**

### How to Use It

**Step 1: Create a TOML configuration**
- Choose the appropriate example from the "Configuration Examples" section below
- Adapt it to the user's app (update `app_module`, `app_class`, interaction steps)
- Use Write tool to create a `.toml` file

**Step 2: Validate with dry-run (recommended)**
```bash
pdm run textual-capture your_config.toml --dry-run
```

**Step 3: Run textual-capture**
```bash
pdm run textual-capture your_config.toml --verbose
```

**Step 4: Analyze output**
- Read the `.txt` files (plain text representation of UI)
- Read the `_tooltips.txt` files (widget metadata and tooltips)
- Optionally mention `.svg` files exist for user to view
- Report findings to user with specific observations

### Configuration Examples

Choose the appropriate template based on the task:

#### 1. Quick UI Review
**When**: User asks "check my UI" or "does this look right?"
**Goal**: Fast LLM analysis of current UI state

```toml
app_module = "user_app_module"
app_class = "UserAppClass"
module_path = "."
formats = ["txt"]                 # Text only - faster for LLM analysis
capture_tooltips = true

[[step]]
type = "capture"
output = "ui_review"
# Analyzes initial state
```

#### 2. Tooltip Accessibility Audit
**When**: User asks about tooltips or accessibility
**Goal**: Find widgets missing tooltips

```toml
app_module = "user_app_module"
app_class = "UserAppClass"
module_path = "."
formats = []                      # Skip rendering - fastest
capture_tooltips = true
tooltip_include_empty = true      # Show widgets without tooltips

[[step]]
type = "capture"
output = "tooltip_audit"
# Check output_tooltips.txt for "(no tooltip)" entries
```

#### 3. Keyboard Navigation Testing
**When**: User wants to verify keyboard shortcuts or tab order
**Goal**: Test multi-step keyboard interaction

```toml
app_module = "user_app_module"
app_class = "UserAppClass"
module_path = "."
formats = ["txt"]

[[step]]
type = "capture"
output = "step_01_initial"

[[step]]
type = "press"
keys = ["tab"]                    # Move to next widget
pause_between = 0.2

[[step]]
type = "capture"
output = "step_02_after_tab"

[[step]]
type = "press"
keys = ["shift+tab"]              # Move back
pause_between = 0.2

[[step]]
type = "capture"
output = "step_03_after_shift_tab"

[[step]]
type = "press"
keys = ["ctrl+s"]                 # Test shortcut
pause_between = 0.2

[[step]]
type = "delay"
seconds = 0.5

[[step]]
type = "capture"
output = "step_04_after_save"
```

#### 4. Documentation Screenshots
**When**: User needs clean visuals for docs or README
**Goal**: Generate SVG screenshots only

```toml
app_module = "user_app_module"
app_class = "UserAppClass"
module_path = "."
output_dir = "./docs/screenshots"
formats = ["svg"]                 # Visual only
capture_tooltips = false          # Don't need tooltips for docs

[[step]]
type = "capture"
output = "main_menu"

[[step]]
type = "press"
keys = ["ctrl+comma"]             # Open settings

[[step]]
type = "delay"
seconds = 0.5

[[step]]
type = "capture"
output = "settings_dialog"
```

#### 5. Full App Exploration
**When**: User asks to "explore the app" or "test all features"
**Goal**: Auto-sequenced captures exploring different states

```toml
app_module = "user_app_module"
app_class = "UserAppClass"
module_path = "."
formats = ["txt"]
capture_tooltips = true

[[step]]
type = "capture"
# Auto: capture_001

[[step]]
type = "press"
keys = ["tab", "tab", "enter"]

[[step]]
type = "delay"
seconds = 0.5

[[step]]
type = "capture"
# Auto: capture_002

[[step]]
type = "click"
label = "Settings"

[[step]]
type = "delay"
seconds = 0.5

[[step]]
type = "capture"
# Auto: capture_003

[[step]]
type = "press"
keys = ["escape"]

[[step]]
type = "capture"
# Auto: capture_004
```

#### 6. Button Click Verification
**When**: User asks to test clicking specific buttons
**Goal**: Verify button interactions work

```toml
app_module = "user_app_module"
app_class = "UserAppClass"
module_path = "."
formats = ["txt"]

[[step]]
type = "capture"
output = "before_click"

[[step]]
type = "click"
label = "Run Selected"            # Button text must match exactly

[[step]]
type = "delay"
seconds = 0.5                     # Wait for action to complete

[[step]]
type = "capture"
output = "after_click"
```

### Best Practices

1. **Use module_path**: Always set `module_path = "."` or appropriate path so imports work
2. **Validate first**: Run with `--dry-run` to catch config errors before execution
3. **Auto-sequence for exploration**: Omit `output` field to auto-generate capture_001, capture_002, etc.
4. **Named captures for specific states**: Use `output = "descriptive_name"` for key moments
5. **Read .txt and _tooltips.txt files**: The text representations are perfect for LLM analysis
6. **Use list syntax for keys**: Prefer `keys = ["tab", "enter"]` over legacy `key = "tab,enter"`
7. **Selective formats**: Use `formats = ["txt"]` for faster LLM analysis, `["svg"]` for visuals only
8. **Tooltip audits**: Use `formats = []` with `capture_tooltips = true` for fast metadata extraction
9. **Verbose mode for debugging**: Use `--verbose` to see what's happening

## Quality Standards

### Test Coverage
- Target: 90% minimum coverage (enforced in CI and `pyproject.toml`)
- Coverage omits: tests, `__pycache__`, `demo*.py` files
- Tests use pytest with async support (`pytest-asyncio`)

### Code Style
- Line length: 120 characters
- Target Python: 3.9+
- Ruff linter with pycodestyle, pyflakes, isort, flake8-bugbear, comprehensions, pyupgrade, simplify
- Exceptions: E501 (line length handled by formatter) and B008 (function calls in defaults, common in Textual)
- MyPy type checking enabled with strict configuration

## Development Notes

### Python Version Support
Requires Python 3.9+ with conditional TOML parser import:
- Python 3.11+: Uses built-in `tomllib`
- Python 3.9-3.10: Falls back to `tomli` package

### Dependencies
- Primary: `textual>=6.11.0`
- Python <3.11: `tomli>=2.0.0` (conditional)
- Dev: `textual-dev>=1.8.0` for Textual development tools
- Test: pytest suite with async and coverage plugins

### CLI Commands

The package provides a `textual-capture` command-line tool:

```bash
# Standard usage
textual-capture config.toml

# Validate without executing
textual-capture config.toml --dry-run

# Show all actions as they execute
textual-capture config.toml --verbose

# Suppress all output except errors
textual-capture config.toml --quiet
```

Installed via `pdm install`, accessible as `pdm run textual-capture` in development.
