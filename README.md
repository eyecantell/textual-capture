# textual-capture

**Sequenced screenshot capture for Textual TUI applications**

[![PyPI - Version](https://img.shields.io/pypi/v/textual-capture?label=PyPI)](https://pypi.org/project/textual-capture/)
[![Python Version](https://img.shields.io/pypi/pyversions/textual-capture)](https://pypi.org/project/textual-capture/)
[![Tests](https://github.com/eyecantell/textual-capture/actions/workflows/ci.yml/badge.svg)](https://github.com/eyecantell/textual-capture/actions)
[![Coverage](https://codecov.io/gh/eyecantell/textual-capture/graph/badge.svg)](https://codecov.io/gh/eyecantell/textual-capture)
[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](https://opensource.org/licenses/MIT)

`textual-capture` lets you define **reproducible sequences** of interactions (key presses, clicks, delays) in your Textual apps and automatically capture **multiple SVG + text snapshots** at key moments.

Perfect for:
- **🤖 LLM-driven TUI review and testing** (primary use case!)
- Creating consistent documentation screenshots
- Building demos and tutorials
- Generating "before/after" visuals for READMEs
- Visual regression prep (pair with snapshot testing)

Unlike single-shot tools, `textual-capture` supports **multi-step sequences** defined in clean, readable TOML files.

---

### Keyboard Navigation and Modifiers

**Advanced key press control with list syntax and modifiers:**

```toml
# List syntax (preferred for multiple keys)
[[step]]
type = "press"
keys = ["tab", "tab", "enter"]

# Modifier combinations
[[step]]
type = "press"
keys = ["ctrl+s"]           # Save shortcut

# Multiple modifiers
[[step]]
type = "press"
keys = ["ctrl+shift+p"]     # Command palette

# Custom timing between keys
[[step]]
type = "press"
keys = ["down", "down", "down"]
pause_after = 0.3           # Wait 0.3s between each key (default: 0.2s)

# Legacy comma-separated syntax (still supported)
[[step]]
type = "press"
key = "tab,ctrl+c,ctrl+v"
```

**Supported modifiers**: `ctrl+`, `shift+`, `alt+`, `meta+`

---

### Capture Tooltips

**Tooltips are automatically captured with every screenshot** (enabled by default). This creates a `{name}_tooltips.txt` file alongside your SVG and text captures.

```toml
# Basic capture (tooltips enabled by default)
[[step]]
type = "capture"
output = "dashboard"
# Creates: dashboard.svg, dashboard.txt, dashboard_tooltips.txt

# Disable tooltips for a specific capture
[[step]]
type = "capture"
output = "quick_visual"
capture_tooltips = false

# Disable tooltips globally
capture_tooltips = false

# Capture only specific widgets
[[step]]
type = "capture"
output = "button_tooltips"
tooltip_selector = "Button"    # Only capture Button widgets

# Include widgets without tooltips
[[step]]
type = "capture"
output = "complete_audit"
tooltip_include_empty = true   # Show "(no tooltip)" for widgets without tooltips
```

**Tooltip file format:**
```
# Tooltips captured from: dashboard
# Selector: *
# Timestamp: 2025-12-20 10:30:45

Button#run: Start the selected command
Button#cancel: Abort current operation (Esc)
Input#search: Search for items
Label#status: (no tooltip)
```

**Tooltip-only captures** (skip visual rendering for speed):
```toml
formats = []              # Don't generate SVG or TXT
capture_tooltips = true

[[step]]
type = "capture"
output = "metadata_only"
# Creates only: metadata_only_tooltips.txt
```

**Use cases:**
- **LLM UI review**: Text format perfect for AI analysis
- **Accessibility audits**: Verify all interactive elements have tooltips
- **Documentation**: Capture help text alongside visuals
- **Testing**: Validate tooltip content programmatically

---

### Installation

```bash
pip install textual-capture
```

Or with PDM:
```bash
pdm add textual-capture
```

---

### Quick Example

Create a file called `demo_sequence.toml` next to your app:

```toml
app_module = "my_app"
app_class = "MyTextualApp"
screen_width = 90
screen_height = 40

[[step]]
type = "press"
key = "tab,tab,enter"

[[step]]
type = "delay"
seconds = 2.0

[[step]]
type = "capture"
output = "running_state"

[[step]]
type = "press"
key = "q"
```

Then run:

```bash
textual-capture demo_sequence.toml           # Default: quiet mode
textual-capture demo_sequence.toml --verbose # Show all actions
textual-capture demo_sequence.toml --quiet   # Errors only
textual-capture demo_sequence.toml --dry-run # Validate without executing
```

This will:
- Launch your app in test mode
- Press Tab twice, then Enter
- Wait 2 seconds
- Save `running_state.svg` and `running_state.txt`
- Press `q` to quit cleanly

---

### 🤖 LLM-Driven TUI Review

**Primary Use Case**: Enable AI assistants like Claude Code to review and test your TUI applications by capturing screenshots at different states.

**When working with an LLM on a Textual app, the LLM can:**
- Generate TOML configurations on the fly to capture specific UI states
- Automatically verify UI layout changes after code modifications
- Review button placement, labels, and visual hierarchy from text output
- Test interaction sequences without manual intervention

**Example workflow:**
```
User: "I just added a new settings dialog. Can you check if it looks good?"
LLM:  Creates llm_review.toml → Runs textual-capture → Analyzes .txt output →
      Reports: "Settings dialog opens correctly, but Cancel button is off-screen..."
```

See `examples/llm_review.toml` for a template AI assistants can adapt.

**Claude Code Integration**: Copy `CLAUDE_SNIPPET.md` into your project's `CLAUDE.md` to give Claude Code full context on using textual-capture for your TUI app.

---

### Why textual-capture?

| Feature                        | textual-dev screenshot | pytest-textual-snapshot | **textual-capture** |
|-------------------------------|-------------------------|--------------------------|---------------------|
| Single capture                | Yes                     | Yes                      | Yes                 |
| Multi-step interaction sequences | No                      | No                       | Yes                 |
| Click buttons by label        | No                      | No                       | Yes                 |
| Delays between actions        | No                      | No                       | Yes                 |
| Multiple timed captures       | No                      | No                       | Yes                 |
| Human-readable config (TOML)  | No                      | No                       | Yes                 |
| Dry-run validation            | No                      | No                       | Yes                 |
| Configurable output directory | No                      | No                       | Yes                 |
| Selective format generation   | No                      | No                       | Yes                 |
| Works with any Textual app    | Yes                     | Yes                      | Yes                 |

---

### Configuration Options

In your `.toml` file:

```toml
# Required fields
app_module = "path.to.module"      # Module containing your Textual app
app_class = "MyApp"                # Textual App class name

# Optional configuration
screen_width = 100                 # Terminal width (default: 80)
screen_height = 40                 # Terminal height (default: 40)
initial_delay = 1.0                # Wait before first action (default: 1.0)
scroll_to_top = true               # Press "home" at start (default: true)
module_path = "path/to/modules"    # Add to sys.path for imports (optional)

# Output configuration
output_dir = "./screenshots"       # Directory for all captures (default: ".")
formats = ["svg", "txt"]           # Default formats (default: ["svg", "txt"])

# Tooltip configuration
capture_tooltips = true            # Capture tooltips with screenshots (default: true)
tooltip_selector = "*"             # CSS selector for widgets (default: "*" = all)
tooltip_include_empty = false      # Include widgets without tooltips (default: false)

# Action steps
[[step]]
type = "press"                     # Press keyboard keys
key = "tab,down,enter"             # Comma-separated keys (legacy)
keys = ["tab", "ctrl+s"]           # List syntax (preferred for multiple keys)
pause_after = 0.2                  # Seconds between keys (default: 0.2)

[[step]]
type = "click"                     # Click a button
label = "Run Selected"             # Button text (spaces removed for ID)

[[step]]
type = "delay"                     # Pause for timing
seconds = 1.5                      # Seconds to wait

[[step]]
type = "capture"                   # Take screenshot
output = "my_state"                # Optional: custom name (saves my_state.svg + .txt + _tooltips.txt)
formats = ["svg"]                  # Optional: override global formats for this capture
capture_tooltips = true            # Optional: override global tooltip setting
tooltip_selector = "Button"        # Optional: custom selector for this capture
                                   # If output omitted: auto-generates capture_001.svg, etc.
```

---

### Output Organization

**Organize captures with `output_dir`:**

```toml
# Keep your project root clean
output_dir = "./screenshots"

[[step]]
type = "capture"
output = "dashboard"
```

Result: Creates `./screenshots/dashboard.svg` and `./screenshots/dashboard.txt`

The output directory is created automatically if it doesn't exist, including any parent directories.

---

### Selective Format Generation

**Control which formats are generated:**

```toml
# Global default - applies to all captures
formats = ["svg"]  # Only generate SVG files

[[step]]
type = "capture"
output = "quick_check"
# Uses global setting: svg only

[[step]]
type = "capture"
output = "detailed_view"
formats = ["svg", "txt"]  # Override: generate both for this capture
```

**Valid formats**: `svg`, `txt`

**Use cases:**
- **SVG only** (`formats = ["svg"]`): Faster execution, visual documentation
- **TXT only** (`formats = ["txt"]`): LLM review workflows, automated analysis
- **Both** (`formats = ["svg", "txt"]`): Complete documentation (default)

**Benefits:**
- ~50% faster when using single format
- Reduces file clutter
- Optimizes for specific workflows (visual vs. programmatic review)

---

### Dry-Run Validation

**Validate configurations without executing:**

```bash
textual-capture sequence.toml --dry-run
```

Output shows:
- Configuration summary
- Planned execution steps with details
- Auto-generated capture names
- Module import validation
- Success/failure status

**Example output:**
```
Configuration: demo_sequence.toml
App: my_app.MyApp
Screen: 90x40
Output Directory: ./screenshots
Default Formats: svg, txt
Initial Delay: 2.0s
Scroll to Top: True

Planned Steps (4 total):
  1. press: keys="tab,tab,enter"
  2. delay: 2.0s
  3. capture: output="running_state", formats=[svg, txt]
  4. press: keys="q"

Validating module import...
✓ Successfully imported MyApp from my_app

✓ Configuration valid and ready to execute
```

**Use dry-run for:**
- Debugging complex sequences
- CI/CD validation pipelines
- Sharing sequences with others or LLMs
- Quick syntax checking

---

### Auto-Sequencing

**Omit the `output` field to automatically generate sequential filenames:**

```toml
[[step]]
type = "capture"
# Auto-generates: capture_001.svg, capture_001.txt

[[step]]
type = "press"
key = "down"

[[step]]
type = "capture"
# Auto-generates: capture_002.svg, capture_002.txt

[[step]]
type = "capture"
output = "named_state"
# Uses explicit name: named_state.svg, named_state.txt

[[step]]
type = "capture"
# Auto-generates: capture_003.svg, capture_003.txt (counter continues)
```

Mix and match named and auto-sequenced captures as needed!

---

### Common Workflows

#### Fast Visual Documentation
```toml
output_dir = "./docs/screenshots"
formats = ["svg"]  # Visual only, 50% faster

[[step]]
type = "capture"
# Quick captures without text overhead
```

#### LLM-Driven Analysis
```toml
output_dir = "./llm_review"
formats = ["txt"]           # Text representation
capture_tooltips = true     # Plus tooltips

[[step]]
type = "press"
keys = ["tab", "enter"]

[[step]]
type = "capture"
# Creates text files LLMs can easily analyze
```

#### Tooltip-Only Audit
```toml
output_dir = "./tooltip_audit"
formats = []                     # Skip visual rendering
capture_tooltips = true
tooltip_include_empty = true     # Show all widgets

[[step]]
type = "capture"
output = "all_tooltips"
# Fast metadata extraction: all_tooltips_tooltips.txt
```

#### Complete Documentation
```toml
output_dir = "./screenshots"
formats = ["svg", "txt"]     # Default: both formats
capture_tooltips = true      # Plus tooltips

[[step]]
type = "capture"
output = "feature_demo"
# Full documentation: SVG + TXT + tooltips
```

#### Keyboard Shortcut Testing
```toml
# Test complex keyboard workflows
[[step]]
type = "press"
keys = ["ctrl+n"]           # New file

[[step]]
type = "delay"
seconds = 0.5

[[step]]
type = "press"
keys = ["t", "e", "s", "t"]
pause_after = 0.1           # Slow typing

[[step]]
type = "press"
keys = ["ctrl+s"]           # Save

[[step]]
type = "capture"
output = "after_save"
```

---

### Contributing

Contributions are welcome! See [CONTRIBUTING.md](CONTRIBUTING.md) (coming soon).

Issues and feature requests: https://github.com/eyecantell/textual-capture/issues

---

### License

MIT © 2025 Paul Neumann