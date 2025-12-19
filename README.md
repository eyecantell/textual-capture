# textual-capture

**Sequenced screenshot capture for Textual TUI applications**

[![PyPI - Version](https://img.shields.io/pypi/v/textual-capture?label=PyPI)](https://pypi.org/project/textual-capture/)
[![Python Version](https://img.shields.io/pypi/pyversions/textual-capture)](https://pypi.org/project/textual-capture/)
[![Tests](https://github.com/eyecantell/textual-capture/actions/workflows/ci.yml/badge.svg)](https://github.com/eyecantell/textual-capture/actions)
[![Coverage](https://codecov.io/gh/eyecantell/textual-capture/graph/badge.svg)](https://codecov.io/gh/eyecantell/textual-capture)
[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](https://opensource.org/licenses/MIT)

`textual-capture` lets you define **reproducible sequences** of interactions (key presses, clicks, delays) in your Textual apps and automatically capture **multiple SVG + text snapshots** at key moments.

Perfect for:
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
textual-capture demo_sequence.toml
```

This will:
- Launch your app in test mode
- Press Tab twice, then Enter
- Wait 2 seconds
- Save `running_state.svg` and `running_state.txt`
- Press `q` to quit cleanly

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
app_module = "path.to.module"      # Required
app_class = "MyApp"                # Required
screen_width = 100                 # Optional (default: 80)
screen_height = 40                 # Optional (default: 40)
initial_delay = 1.0                # Optional
scroll_to_top = true               # Optional (press "home" at start)

[[step]]
type = "press" | "click" | "delay" | "capture"

# press: comma-separated keys
key = "tab,down,enter"

# click: button label (spaces removed for ID matching)
label = "Run Selected"

# delay in seconds
seconds = 1.5

# capture: output base name
output = "my_state"  # saves my_state.svg + my_state.txt
```

---

### Contributing

Contributions are welcome! See [CONTRIBUTING.md](CONTRIBUTING.md) (coming soon).

Issues and feature requests: https://github.com/eyecantell/textual-capture/issues

---

### License

MIT © 2025 Paul Neumann
```