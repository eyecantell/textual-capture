"""
Simple demo Textual application for testing textual-capture.

This minimal app demonstrates the key features that can be captured:
- Keyboard navigation (tab, enter)
- Button interactions
- Visual state changes

Run standalone:
    python examples/demo_app.py

Or capture with textual-capture:
    textual-capture examples/basic.toml
"""

from textual.app import App, ComposeResult
from textual.containers import Container
from textual.widgets import Button, Footer, Header, Label, Static


class DemoApp(App[None]):
    """A simple demo application for screenshot capture testing."""

    CSS = """
    Container {
        height: auto;
        padding: 1 2;
    }

    #status {
        margin: 1 0;
        padding: 1 2;
        background: $boost;
        border: solid $primary;
    }

    Button {
        margin: 1 2;
    }
    """

    BINDINGS = [
        ("q", "quit", "Quit"),
    ]

    def __init__(self):
        super().__init__()
        self.status_text = "Ready to start..."

    def compose(self) -> ComposeResult:
        """Create child widgets for the app."""
        yield Header()
        yield Container(
            Label("Welcome to the Demo App", id="title"),
            Static(self.status_text, id="status"),
            Button("Run Selected", id="RunSelected"),
            Button("Cancel", id="Cancel"),
        )
        yield Footer()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle button presses."""
        button_id = event.button.id
        if button_id == "RunSelected":
            self.update_status("Running selected operation...")
        elif button_id == "Cancel":
            self.update_status("Operation cancelled")

    def update_status(self, message: str) -> None:
        """Update the status message."""
        self.status_text = message
        status_widget = self.query_one("#status", Static)
        status_widget.update(message)


def main():
    """Run the demo app."""
    app = DemoApp()
    app.run()


if __name__ == "__main__":
    main()
