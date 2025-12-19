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

# Action steps
[[step]]
type = "press"                     # Press keyboard keys
key = "tab,down,enter"             # Comma-separated keys

[[step]]
type = "click"                     # Click a button
label = "Run Selected"             # Button text (spaces removed for ID)

[[step]]
type = "delay"                     # Pause for timing
seconds = 1.5                      # Seconds to wait

[[step]]
type = "capture"                   # Take screenshot
output = "my_state"                # Optional: custom name (saves my_state.svg + .txt)
                                   # If omitted: auto-generates capture_001.svg, capture_002.svg, etc.
```

**Auto-sequencing**: Omit the `output` field in capture actions to automatically generate sequential filenames (`capture_001`, `capture_002`, etc.). Mix and match named and auto-sequenced captures as needed!

---

### Contributing

Contributions are welcome! See [CONTRIBUTING.md](CONTRIBUTING.md) (coming soon).

Issues and feature requests: https://github.com/eyecantell/textual-capture/issues

---

### License

MIT © 2025 Paul Neumann
