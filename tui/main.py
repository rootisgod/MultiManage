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
from textual.app import App, ComposeResult, events
from textual.widgets import Header, Footer, DataTable, Input, Button, Label, RichLog
from textual.widgets.data_table import RowDoesNotExist


# https://textual.textualize.io/tutorial/
class mptui(App):
    """A Textual app to manage multipass."""

    BINDINGS = [("[", "stop_instance", "Stop"),
                ("]", "start_instance", "Start"),
                ("p", "suspend_instance", "Suspend"),
                ("<", "stop_all", "Stop ALL"),
                (">", "start_all", "Start ALL"),
                ("r", "refresh_table", "Refresh Table"),
                ("q", "quit", "QUIT")
                ]

    def compose(self) -> ComposeResult:
        """Create child widgets for the app."""
        yield Header()
        yield DataTable(cursor_type="row")
        yield Label("Value", id="value_label")
        yield RichLog()
        yield Footer()

    def refresh_table(self) -> None:
        rows = get_instances_for_textual_datatable()
        table = self.query_one(DataTable)
        table.clear(columns=True)
        table.add_columns(*rows[0])
        table.add_rows(rows[1:])

    def get_selected_instance_name(self) -> str:
        table = self.query_one(DataTable)
        value = table.get_row_at(table.cursor_row)
        # Name has to 'always' be 0 column
        instance_name = value[0]
        return instance_name

    # Use this to test what values are passed around etc...
    def on_key(self, event: events.Key) -> None:
        table = self.query_one(DataTable)
        value = table.get_row_at(table.cursor_row)
        # Name has to 'always' be 0 column
        instance_name = value[0]
        label = self.query_one(Label)
        label.update(str(instance_name))
        # self.query_one(RichLog).write(event)
        # self.query_one(RichLog).write(str(instance_name))


    def on_mount(self) -> None:
        self.refresh_table()
        # Doesn seem to work
        # self.set_interval(1, self.refresh_table())

    # ACTIONS
    def action_refresh_table(self) -> None:
        """An action to refresh the table"""
        self.refresh_table()

    def action_stop_all(self) -> None:
        """An action to stop all instances"""
        self.notify(f"Stopped ALL Instances")
        stop_all_instances()
        self.refresh_table()

    def action_start_all(self) -> None:
        """An action to start all instances"""
        self.notify(f"Started ALL Instances")
        start_all_instances()
        self.refresh_table()

    def action_start_instance(self) -> None:
        """An action to start the selected instances"""
        instance_name = self.get_selected_instance_name()
        self.notify(f"Started {instance_name}")
        start_instance(instance_name)
        self.refresh_table()

    def action_suspend_instance(self) -> None:
        """An action to suspend the selected instances"""
        instance_name = self.get_selected_instance_name()
        self.notify(f"Suspended {instance_name}")
        suspend_instance(instance_name)
        self.refresh_table()

    def action_stop_instance(self) -> None:
        """An action to stop the selected instances"""
        instance_name = self.get_selected_instance_name()
        self.notify(f"Stopped {instance_name}")
        stop_instance(instance_name)
        self.refresh_table()

    def action_quit(self):
        self.exit()


def get_args():
    """ Get passed args """
    parser = argparse.ArgumentParser(description='Get Help')
    parser.add_argument('-h', '--help', metavar='help',
                        default='Runs a Text Interface for Multipass',
                        help='Info on this util')
    return parser.parse_args()


class PreventApp(App):
    """Demonstrates `prevent` context manager."""

    def compose(self) -> ComposeResult:
        yield Input()
        yield Button("Clear", id="clear")

    def on_button_pressed(self) -> None:
        """Clear the text input."""
        input = self.query_one(Input)
        with input.prevent(Input.Changed):  
            input.value = ""

    def on_input_changed(self) -> None:
        """Called as the user types."""
        self.bell()  

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
