"""
Universal TUI Capture Tool
Works with any Textual app — just point it at a .toml file!

Examples:
  python ./src/textual_capture/capture.py                            # quick single capture (old style)
  python ./src/textual_capture/capture.py --input sequence.toml      # full featured sequence
"""

import asyncio
import argparse
from pathlib import Path
import sys
import tomllib  # Python 3.11+ built-in

async def execute_action(pilot, action):
    t = action.get("type")
    if t == "press":
        keys = action.get("key", "")
        for key in keys.split():
            if key.strip():
                await pilot.press(key.strip())
                await pilot.pause(0.2)
        print(f"Pressed: {keys}")
    elif t == "delay":
        sec = float(action.get("seconds", 0.5))
        await pilot.pause(sec)
        print(f"Delayed {sec}s")
    elif t == "click":
        label = action["label"]
        try:
            button_id = f"Button#{label.replace(' ', '')}"
            await pilot.click(button_id)
            print(f"Clicked: {label}")
        except Exception as e:
            print(f"Could not click '{label}': {e}")
    elif t == "capture":
        base = action.get("output", "snapshot")
        svg = f"{base}.svg"
        txt = f"{base}.txt"
        pilot.app.save_screenshot(svg)
        pilot.app.save_screenshot(txt)
        print(f"Captured → {svg} | {txt}")
    else:
        print(f"Unknown action type: {t}")

async def capture(args):
    # Load config from TOML if provided
    if args.input:
        path = Path(args.input)
        if not path.exists():
            print(f"File not found: {args.input}")
            return
        with open(path, "rb") as f:
            config = tomllib.load(f)

        app_module = config.get("app_module")
        app_class_name = config.get("app_class")
        size = tuple(config.get("size", [80, 40]))
        steps = config.get("step", [])
    else:
        # Old CLI fallback
        app_module = "demo_commandlink"
        app_class_name = "CommandOrchestratorApp"
        size = (80, 40)
        steps = []

    # Add parent dir to path for local imports
    sys.path.insert(0, str(Path(__file__).parent.parent))

    # Dynamic import — robust version
    try:
        module = __import__(app_module, fromlist=[app_class_name])
        AppClass = getattr(module, app_class_name)
    except Exception as e:
        print(f"Failed to import {app_class_name} from {app_module}: {e}")
        return

    app = AppClass()

    async with app.run_test(size=size) as pilot:
        await pilot.pause(1)         # initial render
        await pilot.press("home")
        await pilot.pause(0.3)

        if args.input:
            for step in steps:
                await execute_action(pilot, step)
        else:
            # Old CLI behavior
            if args.keys:
                for key in args.keys.split(','):
                    await pilot.press(key.strip())
                    await pilot.pause(0.2)
            if args.click:
                try:
                    await pilot.click(f"Button#{args.click.replace(' ', '')}")
                    print(f"Clicked: {args.click}")
                except Exception as e:
                    print(f"Could not click: {e}")
            await pilot.pause(args.delay)

            base = args.output.replace('.svg', '').replace('.txt', '')
            svg = f"{base}.svg"
            txt = f"{base}.txt"
            pilot.app.save_screenshot(svg)
            pilot.app.save_screenshot(txt)
            print(f"Captured → {svg} | {txt}")

def main():
    parser = argparse.ArgumentParser(
        description='Universal TUI screenshot capturer',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Quick CLI (kept for backward compatibility):
  python ./src/textual_capture/capture.py --keys "tab,enter" --click "Run Selected" --output demo

Modern TOML workflow:
  python ./src/textual_capture/capture.py --input my_demo.toml
        """
    )
    parser.add_argument('--input', help='Path to .toml sequence file')
    parser.add_argument('--keys', help='Comma-separated keys (old style)')
    parser.add_argument('--click', help='Button label (old style)')
    parser.add_argument('--delay', type=float, default=2.0, help='Final delay (old style)')
    parser.add_argument('--output', default='demo-snapshot', help='Output base name (old style)')
    args = parser.parse_args()
    asyncio.run(capture(args))

if __name__ == "__main__":
    main()