# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Added `capture_prefix` configuration option to customize auto-sequenced capture filenames
  - Default: "capture" (maintains backward compatibility)
  - Example: `capture_prefix = "startup"` creates `startup_001.svg`, `startup_002.svg`, etc.
  - Validates prefix for filesystem-safe characters (rejects `/`, `\`, `:`, `*`, `?`, `"`, `<`, `>`, `|`)
  - Works with all output formats (SVG, TXT, and tooltips)
  - Explicit `output` names ignore the prefix (as expected)
  
## [0.3.0] - 2025-12-21

### Added
- Added tooltips to Button widgets in example demo_app.py
- Added three new example configuration files:
  - `tooltip_audit.toml` - Fast accessibility auditing with formats=[] for tooltip-only captures
  - `keyboard_nav.toml` - Comprehensive keyboard navigation and tab order testing
  - `documentation.toml` - SVG-only screenshot generation for documentation
- Added 6 focused configuration examples to CLAUDE.md with clear "When" and "Goal" labels
- Added CLI Commands section to CLAUDE.md documenting all command-line flags

### Changed
- Updated CLAUDE.md to reflect v0.2.0 API features (was referencing v0.1.0)
- Modernized `basic.toml` example with v0.2.0 syntax:
  - Changed from `key = "tab,enter"` to `keys = ["tab", "enter"]` (list syntax)
  - Added tooltip capture configuration
  - Added format configuration and per-step overrides
  - Added `pause_between` parameter demonstration
  - Added custom `widget_selector` demonstration
- Rewrote `llm_review.toml` with LLM-optimized workflow:
  - Added comprehensive tips section for AI assistants
  - Added advanced examples for tooltip-only and selective widget captures
  - Updated to use modern list syntax for keys
- Enhanced CLAUDE.md documentation:
  - Expanded "When to Use This Tool" with explicit example references
  - Improved "How to Use It" workflow with dry-run validation step
  - Expanded best practices from 5 to 9 items
  - Added detailed TOML configuration structure showing all v0.2.0 features
  - Updated Python version references from 3.10+ to 3.9+
  - Replaced single template with 6 focused use-case examples

### Fixed
- Fixed demo_app.py attempting to add tooltips to Label and Static widgets (not supported in Textual)

## [0.2.0] - 2025-12-19

### Changed
- Changed supported python versions from 3.10+ to 3.9+