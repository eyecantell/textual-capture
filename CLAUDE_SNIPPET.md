## Screen Captures with textual-capture

The `textual-capture` tool enables automated TUI screenshot sequences - perfect for LLM-driven review, documentation, and testing.

```bash
# Run a capture sequence defined in a TOML config
textual-capture config.toml --verbose

# Verbosity options
textual-capture config.toml           # Default: quiet mode
textual-capture config.toml --verbose # Show all actions
textual-capture config.toml --quiet   # Errors only
```

**TOML Configuration Format**:
```toml
# Required fields
app_module = "my_app"                     # Python module name (without .py)
app_class = "MyTextualApp"                # App class to instantiate

# Optional configuration
screen_width = 100                        # Terminal width (default: 80)
screen_height = 40                        # Terminal height (default: 40)
initial_delay = 1.0                       # Wait before first action (default: 1.0)
scroll_to_top = true                      # Press "home" at start (default: true)
module_path = "./src"                     # Path to add to sys.path for imports

# Action steps - executed in order
[[step]]
type = "capture"                          # Take a screenshot
output = "initial_state"                  # Optional: custom name (saves initial_state.svg + .txt)
                                          # If omitted: auto-generates capture_001, capture_002, etc.

[[step]]
type = "delay"
seconds = 1.0                             # Wait for animations/async operations

[[step]]
type = "press"
key = "tab,tab,enter"                     # Comma-separated keys for sequences

[[step]]
type = "click"
label = "Run Selected"                    # Click button by label text

[[step]]
type = "capture"                          # Auto-named: capture_001.svg, capture_001.txt
```

**Available Step Types**:
- `capture`: Take screenshot (`.svg` + `.txt`). Use `output` for custom name or omit for auto-sequence
- `delay`: Wait specified seconds (e.g., `seconds = 1.5`)
- `press`: Simulate key presses. Comma-separated for sequences (e.g., `key = "tab,down,enter"`)
- `click`: Click a button by its label text (e.g., `label = "Submit"`)

**LLM Review Workflow**: Generate TOML configs to capture specific UI states, then analyze the `.txt` output to verify layout, button placement, and visual hierarchy without manual intervention.
