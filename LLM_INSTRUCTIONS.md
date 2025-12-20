## Screen Captures with textual-capture

The `textual-capture` tool enables automated TUI screenshot sequences - perfect for LLM-driven review, documentation, and testing.

### Quick Usage

```bash
# Validate config without running (recommended first step)
textual-capture config.toml --dry-run

# Run the capture sequence
textual-capture config.toml

# Verbosity options
textual-capture config.toml --verbose    # Show all actions
textual-capture config.toml --quiet      # Errors only
```

### Basic TOML Configuration

```toml
# Required fields
app_module = "my_app"                     # Python module name (without .py)
app_class = "MyTextualApp"                # App class to instantiate

# Output configuration
output_dir = "./screenshots"              # Where to save files (default: ".")
formats = ["svg", "txt"]                  # Formats to generate (default: both)

# Tooltip capture (enabled by default)
capture_tooltips = true                   # Auto-capture tooltips with screenshots
widget_selector = "*"                    # CSS selector for widgets (default: all)
tooltip_include_empty = false             # Include widgets without tooltips

# Screen and timing
screen_width = 100                        # Terminal width (default: 80)
screen_height = 40                        # Terminal height (default: 40)
initial_delay = 1.0                       # Wait before first action (default: 1.0)

# Action steps - executed in order
[[step]]
type = "press"
keys = ["tab", "tab", "enter"]            # List syntax (preferred)
pause_between = 0.2                         # Seconds between keys (optional)

[[step]]
type = "delay"
seconds = 1.0                             # Wait for animations/async operations

[[step]]
type = "click"
label = "Run Selected"                    # Click button by label text

[[step]]
type = "capture"
output = "after_click"                    # Custom name (optional)
# Creates: after_click.svg, after_click.txt, after_click_tooltips.txt
```

### Available Step Types

#### capture - Take Screenshot
```toml
[[step]]
type = "capture"
output = "my_state"                       # Optional: custom name
formats = ["svg", "txt"]                  # Optional: override global
capture_tooltips = true                   # Optional: override global
widget_selector = "Button"               # Optional: filter widgets
```
- If `output` omitted: auto-generates `capture_001`, `capture_002`, etc.
- Creates `.svg` (visual), `.txt` (text representation), `_tooltips.txt` (widget tooltips)

#### press - Simulate Key Presses
```toml
[[step]]
type = "press"
keys = ["tab", "ctrl+s", "enter"]         # List syntax (preferred)
pause_between = 0.3                         # Optional: seconds between keys

# Legacy comma-separated syntax still works
key = "tab,ctrl+s,enter"
```
- Supports modifiers: `ctrl+`, `shift+`, `alt+`, `meta+`
- Use list syntax for clarity with multiple keys

#### click - Click Button
```toml
[[step]]
type = "click"
label = "Submit"                          # Button text (spaces removed for ID)
```

#### delay - Wait
```toml
[[step]]
type = "delay"
seconds = 1.5                             # Seconds to wait
```

### LLM Review Workflows

#### Basic UI Review
```toml
app_module = "your_app"
app_class = "YourApp"
formats = ["txt"]                         # Text for AI analysis
capture_tooltips = true                   # Include tooltip data

[[step]]
type = "capture"
output = "initial_state"

[[step]]
type = "press"
keys = ["tab", "enter"]

[[step]]
type = "capture"
output = "after_interaction"
```

Then analyze: `cat screenshots/*.txt`

#### Tooltip Audit
```toml
formats = []                              # Skip visual rendering (faster)
capture_tooltips = true
tooltip_include_empty = true              # Show missing tooltips

[[step]]
type = "capture"
output = "tooltip_audit"
```

Check `tooltip_audit_tooltips.txt` for widgets with `(no tooltip)`.

#### Auto-Exploration
```toml
formats = ["txt"]
capture_tooltips = true

[[step]]
type = "capture"
# Auto: capture_001.svg, capture_001.txt, capture_001_tooltips.txt

[[step]]
type = "press"
keys = ["tab"]

[[step]]
type = "capture"
# Auto: capture_002.svg, capture_002.txt, capture_002_tooltips.txt

# Continue exploring...
```

### Tooltip File Format

Tooltips are captured in a structured text format:

```
# Tooltips captured from: my_state
# Selector: *
# Timestamp: 2025-12-20 10:30:45

Button#run: Start the selected command
Button#cancel: Abort current operation (Esc)
Input#search: Search for items
Label#status: (no tooltip)
```

Perfect for parsing and analysis!

### When to Use textual-capture

**Use textual-capture when:**
- User asks to "check the UI", "review the layout", "see what it looks like"
- User wants screenshots or documentation of TUI states
- User asks about tooltips, button placement, or visual hierarchy
- User wants to test keyboard navigation or click sequences
- User needs to verify UI changes after code modifications

**Workflow:**
1. Create TOML config based on user's request
2. Run with `--dry-run` to validate
3. Execute capture
4. Read `.txt` and `_tooltips.txt` files
5. Report findings to user

**Pro Tips:**
- Use `--dry-run` first to catch config errors
- Use `formats = ["txt"]` for faster AI analysis
- Use `tooltip_include_empty = true` for accessibility audits
- Use auto-sequencing (omit `output`) for exploration
- Use `output_dir` to keep files organized

### Configuration Examples

#### Documentation Screenshots
```toml
output_dir = "./docs/screenshots"
formats = ["svg"]                         # Visual only

[[step]]
type = "capture"
output = "main_menu"
```

#### Keyboard Shortcut Testing
```toml
[[step]]
type = "press"
keys = ["ctrl+n"]                         # New dialog

[[step]]
type = "delay"
seconds = 0.5

[[step]]
type = "press"
keys = ["t", "e", "s", "t"]
pause_between = 0.1                         # Slow typing

[[step]]
type = "press"
keys = ["ctrl+s"]                         # Save

[[step]]
type = "capture"
```

#### Button Click Testing
```toml
[[step]]
type = "click"
label = "Settings"

[[step]]
type = "delay"
seconds = 0.3

[[step]]
type = "capture"
output = "settings_dialog"
```

### Common Issues

**Import errors**: Use `module_path` to add directories to sys.path
```toml
module_path = "./src"                     # Or "." for current directory
```

**Button not found**: Check button label matches exactly (case-sensitive)
```toml
[[step]]
type = "click"
label = "Run Selected"                    # Must match button text exactly
```

**Timing issues**: Increase delays for animations or async operations
```toml
[[step]]
type = "delay"
seconds = 2.0                             # Give more time
```

**No widgets in tooltip file**: Use `tooltip_include_empty = true` to see all widgets
```toml
tooltip_include_empty = true              # Show "(no tooltip)" for empty ones
```

### Advanced: Selective Tooltip Capture

Capture tooltips from specific widget types:

```toml
[[step]]
type = "capture"
output = "button_tooltips"
widget_selector = "Button"               # Only buttons

[[step]]
type = "capture"
output = "input_tooltips"
widget_selector = "Input"                # Only inputs

[[step]]
type = "capture"
output = "important_tooltips"
widget_selector = ".important"           # CSS class selector
```

### File Outputs

Each capture creates up to 3 files:

- `{output}.svg` - Visual screenshot (if `formats` includes "svg")
- `{output}.txt` - Text representation (if `formats` includes "txt")
- `{output}_tooltips.txt` - Widget tooltips (if `capture_tooltips = true`)

For LLM analysis, read the `.txt` and `_tooltips.txt` files - they contain structured text perfect for parsing!