from dataclasses import dataclass, field
import logging
from typing import Any, List, Optional

from prompt_toolkit import Application
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.layout import ConditionalContainer, Dimension
from prompt_toolkit.layout.containers import HSplit, Window
from prompt_toolkit.layout.controls import FormattedTextControl
from prompt_toolkit.layout.layout import Layout
from prompt_toolkit.widgets import TextArea
from rich.box import ROUNDED
from rich.console import Console, Group
from rich.panel import Panel
from rich.table import Table

from filet.cli.utils.to_ansi import to_ansi
import filet.patches.typer as typer

# Initialize logger for the module
logger = logging.getLogger(__name__)

# Create a Typer group for CLI commands under 'add'
add_group = typer.Typer(
    name="add",
)


@dataclass
class PromptSelection:
    """Class to manage prompt selections with rich visuals and interactive controls."""

    title: str  # Title for the selection prompt
    description: str = ""  # Optional description for the selection prompt
    kb: KeyBindings = KeyBindings()  # Key bindings for navigation
    search_description_area: TextArea = TextArea(multiline=False)  # Area to display the description
    text_control: FormattedTextControl = FormattedTextControl()  # Control for displaying the list
    visible_count: int = 10  # Number of items visible at once in the list
    # Following fields are initialized in __post_init__ due to their dependency on runtime values
    search_area: TextArea = field(default_factory=TextArea, init=False)  # Text area for search input
    search_area_container: Optional[ConditionalContainer] = field(default=None, init=False)  # Container for search area
    text_window: Optional[Window] = field(default=None, init=False)  # Window to display the selected items
    layout: Optional[Layout] = field(default=None, init=False)  # Layout of the application
    app: Optional[Application] = field(default=None, init=False)  # The prompt_toolkit application
    selection: List[str] = field(default_factory=list)  # List of selectable items
    filtered: List[int] = field(default_factory=list)  # Filtered indices based on search
    displayed: List[int] = field(default_factory=list)  # Indices of items currently displayed
    scroll_offset: int = 0  # Scroll offset for the display window
    selected_index: int = 0  # Currently selected item index
    selected_obj: Any = None  # Object that is currently selected
    console: Console = Console()  # Rich console for rendering tables

    def __post_init__(self):
        """Initializes dynamic components of the class after instance creation."""
        # Initialize dynamic fields with their actual components
        self.search_area = TextArea(multiline=False)
        self.search_area_container = ConditionalContainer(
            content=HSplit([self.search_area, self.search_description_area]), filter=True
        )  # Initially visible
        self.text_window = Window(content=self.text_control, height=Dimension(preferred=self.visible_count + 10))
        # Create a buffer for the application's output
        self.layout = Layout(HSplit([self.search_area_container, self.text_window]))
        self.app = Application(layout=self.layout, key_bindings=self.kb, full_screen=False)

        # Define key bindings for navigation and selection
        @self.kb.add("left")
        def move_left(event):
            """Move the selection down in the list, adjusting the scroll offset if necessary."""
            self.text_control.text = ""
            self.search_area_container.filter = lambda: False
            self.text_window.height = Dimension(preferred=0)
            event.app.exit()

        # Define key bindings for navigation and selection
        @self.kb.add("down")
        def move_down(_):
            """Move the selection down in the list, adjusting the scroll offset if necessary."""
            if self.selected_index < len(self.displayed) - 1:
                self.selected_index += 1
            else:
                self.scroll_offset += 1
            self.update_filter()

        @self.kb.add("up")
        def move_up(_):
            """Move the selection up in the list, adjusting the scroll offset if necessary."""
            if self.selected_index > 0:
                self.selected_index -= 1
            else:
                self.scroll_offset -= 1
            self.update_filter()

        @self.kb.add("enter")
        def select(event):
            """Select the current item and update the display to show the selection."""
            if self.displayed:
                selected_index = self.displayed[self.selected_index]
                self.selected_obj = self.selection[selected_index]
                self.text_control.text = ""
                # self.text_control.text = to_ansi(
                #     Text(f"[{self.title}:", style="bold blue"), selected_index, self.selected_obj, style="bold"
                # )
                self.search_area_container.filter = lambda: False
                self.text_window.height = Dimension(preferred=0)
                event.app.exit()

        # Define key bindings for exiting the application
        @self.kb.add("c-c")
        @self.kb.add("c-q")
        @self.kb.add("c-d")
        def exit_(event):
            """Exit the application."""
            self.text_control.text = ""
            self.search_area_container.filter = lambda: False
            self.text_window.height = Dimension(preferred=0)
            event.app.exit()

        self.reset()

    def reset(self):
        """Reset the search area and filters to their default state."""
        self.search_area_container.filter = lambda: False
        self.search_area.text = ""
        self.filtered = list(range(len(self.selection)))
        self.displayed = self.filtered.copy()
        self.search_area.buffer.on_text_changed.add_handler(lambda _: self.update_filter())
        self.search_area.buffer.on_cursor_position_changed.add_handler(lambda _: self.update_filter())
        self.update_content()

    def update_content(self):
        """Update the content of the display based on the current filter and scroll position."""
        if self.filtered:
            if self.scroll_offset < 0:
                self.scroll_offset = len(self.filtered) - len(self.displayed)
                self.selected_index = len(self.displayed) - 1

            if self.scroll_offset > len(self.filtered) - len(self.displayed):
                self.scroll_offset = 0
                self.selected_index = 0

            if self.selected_index > len(self.displayed) - 1:
                self.selected_index = len(self.displayed) - 1

        # Determine the subset of filtered to display
        self.displayed = self.filtered[self.scroll_offset : self.scroll_offset + self.visible_count]

        # Generate the rich table for display
        search_table_text = self.generate_search_table_view()
        # Update the filtered list display
        list_table_text = self.generate_control_list_view()
        # Combine the tables for display in the text control
        self.text_control.text = to_ansi(Group(search_table_text, list_table_text))
        # self.text_control.text = self.generate_control_list_view()
        # Make sure to refresh the layout to reflect the changes
        self.app.invalidate()

    def generate_search_table_view(self):
        """Generate a rich table view for displaying the current search filter text, underlining a specific character."""
        search_text = self.search_area.text
        cursor_position = self.search_area.buffer.cursor_position

        # Use rich formatting to underline the character at the cursor position
        # Check if cursor_position is within the bounds of the search_text
        if 0 <= cursor_position < len(search_text):
            # Apply underline style to the character at cursor_position
            search_text_with_cursor = (
                f"[bold magenta]{search_text[:cursor_position]}"
                f"[underline green]{search_text[cursor_position]}[/underline green]"
                f"{search_text[cursor_position + 1:]}"
            )
        else:
            # If the cursor is at the end or the text is empty, no need to underline anything
            search_text_with_cursor = "[bold magenta]" + search_text + "[underline green] [/underline green]"

        # Render the table using the rich console, converting it to ANSI for prompt_toolkit
        return Panel(
            "[bright_yellow]Search: " + search_text_with_cursor, title=self.title, subtitle=self.description, width=80
        )

    def update_filter(self):
        """Update the filter based on the search query, adjusting displayed items accordingly."""
        search_result = self.search_area.document.text
        self.filtered = [idx for idx, obj in enumerate(self.selection) if search_result.lower() in obj.lower()]
        self.displayed = self.filtered[: self.visible_count]
        self.update_content()

    def generate_control_list_view(self):
        """Generate a rich table view of the current display list."""
        table = Table(expand=True, box=ROUNDED, padding=0)
        table.add_column("ID", style="cyan")
        table.add_column("Object", style="magenta")

        for idx in self.displayed:
            style = (
                "green bold"
                if (
                    self.displayed
                    and self.selected_index < len(self.displayed)
                    and idx == self.displayed[self.selected_index]
                )
                else ""
            )
            table.add_row(str(idx), self.selection[idx], style=style)

        return Panel(table, width=80)

    def run(self, force_selection=False):
        """Run the prompt_toolkit application to display the selection prompt."""

        if len(self.selection) == 1 and not force_selection:
            self.selected_obj = self.selection[0]
        else:
            self.app.run()
