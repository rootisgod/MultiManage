# Written with Textual 0.52.1

from textual.app import App, ComposeResult
from textual.containers import Container
from textual.screen import ModalScreen
from textual.widgets import Label, Footer
from textual.app import App, ComposeResult
from textual.widgets import DataTable

ROWS = [
    ("lane", "swimmer", "country", "time"),
    (4, "Joseph Schooling", "Singapore", 50.39),
    (2, "Michael Phelps", "United States", 51.14),
    (5, "Chad le Clos", "South Africa", 51.14),
    (6, "László Cseh", "Hungary", 51.14),
    (3, "Li Zhuhao", "China", 51.26),
    (8, "Mehdy Metella", "France", 51.58),
    (7, "Tom Shields", "United States", 51.73),
    (1, "Aleksandr Sadovnikov", "Russia", 51.84),
    (10, "Darren Burns", "Scotland", 51.84),
]

class HelpScreen(ModalScreen[None]):
    BINDINGS = [("escape", "pop_screen")]

    def compose(self) -> ComposeResult:
        with Container(id="help-screen-container"):
            yield Label("This is the help screen.")
            yield Label("You've been helped.")
            yield Label("Press ESC to exit.", id="exit")


class MyApp(App[None]):
    BINDINGS = [("h", "get_help", "Help")]

    def compose(self) -> ComposeResult:
        yield Label("This is my app.")
        yield DataTable()
        yield Footer()

    def action_get_help(self) -> None:
        self.push_screen(HelpScreen())

    def on_mount(self) -> None:
        table = self.query_one(DataTable)
        table.add_columns(*ROWS[0])
        table.add_rows(ROWS[1:])


if __name__ == "__main__":
    app = MyApp()
    app.run()
