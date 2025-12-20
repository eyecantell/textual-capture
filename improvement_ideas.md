# textual-capture Improvement Suggestions

### 1. Output Directory Configuration
Would be useful to specify output directory:
```toml
# Proposed config option
output_dir = "./screenshots"
```

### 2. Selective Capture Formats
Currently generates both `.svg` and `.txt` for every capture. Would be nice to specify format:
```toml
# Proposed: only generate SVG
formats = ["svg"]
```

### 3. Wait for Condition Step
Instead of fixed delays, wait for specific conditions:
```toml
[[step]]
type = "wait_for"
selector = "CommandLink"
attribute = "running"
value = false
timeout = 10.0
```

### 4. Focus Step
Ability to focus a specific widget before capture:
```toml
[[step]]
type = "focus"
selector = "#test-command"
```

### 5. Hover Step
Ability to hover over a widget to trigger tooltip display for capture:
```toml
[[step]]
type = "hover"
selector = "#test-command"  # Hover by CSS selector

[[step]]
type = "hover"
label = "Test"              # Hover by label text (like click)
```
This would allow capturing tooltips in screenshots for documentation.

### 6. Key Modifier Combos
Support for modifier key combinations:
```toml
[[step]]
type = "press"
key = "ctrl+c"
```

### 7. Verbose Output Improvements
When `--verbose`, show more context:
- Widget tree at start
- Current focus after each step
- Whether animations are running

### 8. Dry Run Mode
```bash
pdm run textual-capture config.toml --dry-run
```
Would validate TOML and show planned steps without actually running the app.