"""
Textual Capture - Sequenced screenshot capture for Textual TUI applications.

Automates interaction sequences (key presses, clicks, delays) and captures
multiple screenshots at key moments. Configured via TOML files.

Usage:
    textual-capture sequence.toml              # Quiet mode (errors only)
    textual-capture sequence.toml --verbose    # Show all actions
    textual-capture sequence.toml --quiet      # Suppress all output
"""

import argparse
import asyncio
import logging
import sys
from pathlib import Path
from typing import Any

# Python 3.10 compatibility - tomllib added in 3.11
try:
    import tomllib
except ModuleNotFoundError:
    import tomli as tomllib

# Configure logging
logger = logging.getLogger("textual_capture")


async def execute_action(pilot: Any, action: dict[str, Any], capture_counter: dict[str, int]) -> None:
    """
    Execute a single action in the sequence.

    Args:
        pilot: Textual pilot instance for controlling the app
        action: Action configuration dict with 'type' and action-specific fields
        capture_counter: Mutable dict tracking number of captures (for auto-sequencing)

    Raises:
        ValueError: If action type is unknown or required fields are missing
    """
    action_type = action.get("type")

    if action_type == "press":
        keys = action.get("key", "")
        if not keys:
            logger.warning("press action has no keys specified")
            return

        # Split on commas (README API), strip whitespace
        for key in keys.split(","):
            key = key.strip()
            if key:
                await pilot.press(key)
                await pilot.pause(0.2)
        logger.info(f"Pressed keys: {keys}")

    elif action_type == "delay":
        seconds = float(action.get("seconds", 0.5))
        await pilot.pause(seconds)
        logger.info(f"Delayed {seconds}s")

    elif action_type == "click":
        label = action.get("label")
        if not label:
            raise ValueError("click action missing required 'label' field")

        try:
            # Textual button ID is ButtonLabel without spaces
            button_id = f"Button#{label.replace(' ', '')}"
            await pilot.click(button_id)
            logger.info(f"Clicked button: {label}")
        except Exception as e:
            logger.error(f"Could not click button '{label}': {e}")
            raise

    elif action_type == "capture":
        # Auto-sequencing: if output not specified, generate sequential name
        output = action.get("output")
        if not output:
            capture_counter["count"] += 1
            output = f"capture_{capture_counter['count']:03d}"

        svg_path = f"{output}.svg"
        txt_path = f"{output}.txt"

        pilot.app.save_screenshot(svg_path)
        pilot.app.save_screenshot(txt_path)
        logger.info(f"Captured screenshots: {svg_path}, {txt_path}")

    else:
        raise ValueError(f"Unknown action type: {action_type}")


def validate_config(config: dict[str, Any]) -> None:
    """
    Validate TOML configuration before execution.

    Args:
        config: Parsed TOML configuration dict

    Raises:
        ValueError: If required fields are missing or invalid
    """
    # Required fields
    if "app_module" not in config:
        raise ValueError("TOML config missing required field: 'app_module'")
    if "app_class" not in config:
        raise ValueError("TOML config missing required field: 'app_class'")

    # Validate action steps
    steps = config.get("step", [])
    for i, step in enumerate(steps):
        if "type" not in step:
            raise ValueError(f"Step {i}: missing required 'type' field")

        step_type = step["type"]
        valid_types = {"press", "delay", "click", "capture"}
        if step_type not in valid_types:
            raise ValueError(f"Step {i}: invalid type '{step_type}'. Must be one of: {valid_types}")

        # Validate type-specific required fields
        if step_type == "click" and "label" not in step:
            raise ValueError(f"Step {i}: 'click' action missing required 'label' field")


async def capture(toml_path: str) -> None:
    """
    Main capture function - loads TOML config and executes sequence.

    Args:
        toml_path: Path to TOML configuration file

    Raises:
        FileNotFoundError: If TOML file doesn't exist
        ValueError: If TOML is invalid or config is malformed
    """
    # Load and parse TOML
    path = Path(toml_path)
    if not path.exists():
        raise FileNotFoundError(f"TOML file not found: {toml_path}")

    logger.info(f"Loading configuration from: {toml_path}")

    try:
        with open(path, "rb") as f:
            config = tomllib.load(f)
    except Exception as e:
        raise ValueError(f"Failed to parse TOML file: {e}") from e

    # Validate configuration upfront (fail fast)
    validate_config(config)

    # Extract configuration (with defaults matching README)
    app_module = config["app_module"]
    app_class_name = config["app_class"]
    screen_width = config.get("screen_width", 80)
    screen_height = config.get("screen_height", 40)
    initial_delay = config.get("initial_delay", 1.0)
    scroll_to_top = config.get("scroll_to_top", True)
    module_path = config.get("module_path")
    steps = config.get("step", [])

    logger.info(f"App: {app_module}.{app_class_name}")
    logger.info(f"Screen size: {screen_width}x{screen_height}")
    logger.info(f"Steps: {len(steps)} action(s)")

    # Add module_path to sys.path if specified
    if module_path:
        sys.path.insert(0, str(Path(module_path).resolve()))
        logger.info(f"Added to module path: {module_path}")
    else:
        # Default: add parent directory for local imports
        sys.path.insert(0, str(Path(__file__).parent.parent))

    # Dynamic import
    try:
        module = __import__(app_module, fromlist=[app_class_name])
        AppClass = getattr(module, app_class_name)
        logger.info(f"Successfully imported {app_class_name} from {app_module}")
    except ImportError as e:
        raise ImportError(f"Failed to import module '{app_module}': {e}") from e
    except AttributeError as e:
        raise AttributeError(f"Module '{app_module}' has no class '{app_class_name}': {e}") from e

    # Instantiate and run app
    app = AppClass()

    async with app.run_test(size=(screen_width, screen_height)) as pilot:
        # Initial delay for rendering
        await pilot.pause(initial_delay)

        # Scroll to top if requested
        if scroll_to_top:
            await pilot.press("home")
            await pilot.pause(0.3)
            logger.info("Scrolled to top")

        # Execute action sequence
        capture_counter = {"count": 0}  # Mutable for auto-sequencing
        for i, step in enumerate(steps):
            logger.info(f"Executing step {i + 1}/{len(steps)}: {step.get('type')}")
            try:
                await execute_action(pilot, step, capture_counter)
            except Exception as e:
                logger.error(f"Step {i + 1} failed: {e}")
                raise

    logger.info("Sequence completed successfully")


def main() -> None:
    """Main entry point for the CLI."""
    parser = argparse.ArgumentParser(
        prog="textual-capture",
        description="Sequenced screenshot capture for Textual TUI applications",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    textual-capture demo.toml              # Run with default logging (errors only)
    textual-capture demo.toml --verbose    # Show all actions as they execute
    textual-capture demo.toml --quiet      # Suppress all output except errors

Configuration:
    Create a .toml file defining your app and interaction sequence.
    See https://github.com/eyecantell/textual-capture for examples.
        """,
    )

    parser.add_argument("toml_file", help="Path to TOML configuration file")

    parser.add_argument("-v", "--verbose", action="store_true", help="Enable verbose output (show all actions)")

    parser.add_argument("-q", "--quiet", action="store_true", help="Suppress all output except errors")

    args = parser.parse_args()

    # Configure logging based on flags
    if args.quiet:
        log_level = logging.ERROR
    elif args.verbose:
        log_level = logging.INFO
    else:
        log_level = logging.WARNING

    logging.basicConfig(level=log_level, format="%(levelname)s: %(message)s", stream=sys.stderr)

    # Run capture
    try:
        asyncio.run(capture(args.toml_file))
    except KeyboardInterrupt:
        logger.info("Interrupted by user")
        sys.exit(130)
    except Exception as e:
        logger.error(f"Fatal error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
