#!/usr/bin/env python3
"""
Author:  Iain
Purpose: Multipass TU
"""

# Python Files
from functions import *
# Generic Libraries
import argparse
from typing import Dict, Any
# Textual
from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, DataTable


# https://textual.textualize.io/tutorial/
class mptui(App):
    """A Textual app to manage multipass."""

    BINDINGS = [("d", "toggle_dark", "Toggle dark mode"),
                ("!", "stop_all", "Stop ALL"),
                (">", "start_all", "Start ALL"),
                ("s", "start_instance", "Start Instance"),
                ("r", "refresh_table", "Refresh Table")]

    def compose(self) -> ComposeResult:
        """Create child widgets for the app."""
        yield Header()
        yield DataTable(cursor_type="row")
        yield Footer()

    def refresh_table(self) -> None:
        rows = get_instances_for_textual_datatable()
        table = self.query_one(DataTable)
        table.clear(columns=True)
        table.add_columns(*rows[0])
        table.add_rows(rows[1:])

    def on_mount(self) -> None:
        self.refresh_table()

    # ACTIONS
    def action_toggle_dark(self) -> None:
        """An action to toggle dark mode."""
        self.dark = not self.dark

    def action_refresh_table(self) -> None:
        """An action to refresh the table"""
        self.refresh_table()

    def action_stop_all(self) -> None:
        """An action to stop all instances"""
        stop_all_instances()
        self.refresh_table()

    def action_start_all(self) -> None:
        """An action to start all instances"""
        start_all_instances()
        self.refresh_table()

    def action_start_instance(self) -> None:
        """An action to start selected instances"""

        # To make dynamic based on row selected
        start_instance("vm1")
        self.refresh_table()


def get_args():
    """ Get passed args """

    parser = argparse.ArgumentParser(description='Get Help')
    parser.add_argument('-h', '--help', metavar='help',
                        default='Runs a Text Interface for Multipass',
                        help='Info on this util')
    return parser.parse_args()


def main():
    """ Execute program """

    print("*** Program Started ***")
    mp_version = get_multipass_version()
    print(f"MP Version is: {mp_version}")
    print("*** Program Ended ***")
    #-----------------------------------------------------
    app = mptui()
    app.run()
    #-----------------------------------------------------

if __name__ == '__main__':
    main()
