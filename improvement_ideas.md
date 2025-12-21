```markdown
# textual-capture Improvement Suggestions

Prioritized by implementation difficulty (Easiest → Hardest).  
Each item includes estimated effort, rationale, proposed configuration syntax, and notes on value vs. complexity.

### 1. Dry Run Mode  ** Implemented 12/20/2025 **
**Difficulty**: Easy (~30–45 min)  
**Value**: High for development and CI workflows  

Add a `--dry-run` CLI flag that loads and validates the TOML config, then prints a readable summary of all planned steps without launching the app or executing any actions.

**Proposed CLI**:
```bash
textual-capture config.toml --dry-run
```

**Benefits**:
- Immediate feedback on config errors or step planning.
- Safe for CI/validation scripts.
- Useful when sharing sequences with others or with LLMs.

### 2. Output Directory Configuration ** Implemented 12/20/2025 **
**Difficulty**: Easy (~30 min)  
**Value**: High – cleaner project organization  

Allow specifying a base directory for all captures.

**Proposed TOML**:
```toml
output_dir = "./screenshots"  # Default: current working directory
```

All capture files (SVG, TXT, and future formats) will be placed here. Directory created automatically if missing.

### 3. Selective Capture Formats ** Implemented 12/20/2025 **
**Difficulty**: Easy (~45 min)  
**Value**: Medium-High – reduces clutter, faster runs  

Currently always saves both `.svg` and `.txt`. Allow choosing which formats to generate globally or per-capture.

**Proposed TOML**:
```toml
# Global default
formats = ["svg", "txt"]  # or ["svg"] / ["txt"]

# Per-step override
[[step]]
type = "capture"
output = "initial_state"
formats = ["svg"]
```

### 4. Key Modifier Combinations ** Implemented 12/20/2025 **
**Difficulty**: Easy (~45 min)  
**Value**: Medium – improves usability for common shortcuts  

Textual’s Pilot already supports modifiers. Remove the current comma-splitting hack and pass keys directly.

**Proposed TOML**:
```toml
[[step]]
type = "press"
key = "ctrl+c"          # Single key with modifiers
# or
keys = ["tab", "ctrl+c", "enter"]  # Array for sequences (recommended for clarity)
```

Backwards compatibility note: keep supporting comma-separated strings for now, but document array as preferred.

### 5. Log Tooltips Programmatically ** Implemented 12/20/2025 **
**Difficulty**: Medium (~1–2 hours)  
**Value**: Very High – especially for LLM-driven review and documentation  

Replace the original fragile “hover to capture tooltip visually” idea with a reliable action that extracts and logs all tooltip text directly from widgets.

**Proposed TOML**:
```toml
[[step]]
type = "log_tooltips"
selector = "Button"          # Optional: CSS selector to limit scope (default: all widgets)
include_empty = false        # Default: true (skip widgets without tooltip)
output = "tooltips"          # Optional: save to tooltips.txt in addition to logging
```

**Example output** (verbose mode or file):
```
Button#run [Run]: Start the selected command
Button#cancel [Cancel]: Abort current operation (Esc)
Input#cmd []: Enter command to execute
```

**Why this wins over visual hover**:
- 100% reliable – no mouse simulation, coordinate math, or timing issues.
- Works automatically on composite widgets (tooltips on children are collected individually).
- Perfect for LLM review: exact text content without needing to interpret screenshots.
- Fast and deterministic.

### 6. Enhanced Verbose Output
**Difficulty**: Medium (~1–1.5 hours)  
**Value**: Medium – great for debugging complex sequences  

When `--verbose` is used, add richer context after each step:
- Current focused widget ID
- Whether any animations are running (`app.animator.is_running`)
- Optional lightweight widget tree summary (top-level nodes only, to avoid noise)

**No config changes needed** – automatic with existing `--verbose` flag.

### 7. Focus Widget Step
**Difficulty**: Medium (~1 hour)  
**Value**: Medium – useful for keyboard navigation testing and tooltip triggering  

Explicitly focus a widget by selector (many tooltips appear on focus, not just hover).

**Proposed TOML**:
```toml
[[step]]
type = "focus"
selector = "#run-button"     # CSS selector or ID
# or
label = "Run"                # Alternative: match by button label (like click)
```

Can be combined with `delay` + `capture` as a reliable tooltip-triggering pattern.

### 8. Wait for Condition Step
**Difficulty**: Medium → Hard (~2–3 hours)  
**Value**: High – eliminates brittle fixed delays  

Wait for a specific widget state instead of using arbitrary pauses.

**Proposed TOML**:
```toml
[[step]]
type = "wait_for"
selector = ".progress-bar"
attribute = "value"
value = 100                  # Can be int, float, bool, or string
timeout = 15.0               # Seconds, default 10.0
poll_interval = 0.2          # Optional
```

Implementation uses polling loop with `pilot.app.query_one()` and `getattr(widget, attribute)`.

### Removed / Deferred
- **Hover Step** (previously #5)  
  **Reason**: Hard, fragile, and low reliability in automated test runner due to mouse coordinate calculation and timing. Replaced by the far superior `log_tooltips` action for content extraction and `focus` + `delay` for visual triggering when needed.

---

These improvements maintain backward compatibility where possible and significantly enhance `textual-capture` for both human and LLM-driven workflows. Recommended implementation order: 1 → 2 → 3 → 4 → 5 (big win) → 6 → 7 → 8.
```