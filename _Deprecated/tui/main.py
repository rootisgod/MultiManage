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
from textual import log, on
from textual.app import App, ComposeResult, events
from textual.containers import Container
from textual.widgets import Header, Footer, DataTable, Input, Button, Label, RichLog
from textual.widgets.data_table import RowDoesNotExist
from textual.screen import ModalScreen
from textual_terminal import Terminal

class HelpScreen(ModalScreen[None]):
    BINDINGS = [("escape", "pop_screen")]

    DEFAULT_CSS = """
    HelpScreen {
        align: center middle;
    }

    #help-screen-container {
        width: auto;
        max-width: 70%;
        height: auto;
        max-height: 80%;
        background: $panel;
        align: center middle;
        padding: 2 4;

        & > Label#exit {
            margin-top: 1;
        }
    }
    """

    def compose(self) -> ComposeResult:
        with Container(id="help-screen-container"):
            yield Label("A MultiPasss Text UI")
            yield Label("Hopefully you find it useful.")
            yield Input()
            yield Label("Press ESC to exit.", id="exit")

    @on(Input.Submitted)
    def on_input_submitted(self):
        input = self.query_one(Input)
        return input.value


# https://textual.textualize.io/tutorial/
class mptui(App):
    """A Textual app to manage multipass."""

    BINDINGS = [
                ("h", "get_help", "Help"),
                ("c", "quick_create_instance", "Quick Create"),
                ("[", "stop_instance", "Stop"),
                ("]", "start_instance", "Start"),
                ("p", "suspend_instance", "Suspend"),
                ("<", "stop_all", "Stop ALL"),
                (">", "start_all", "Start ALL"),
                ("d", "delete_instance", "Delete"),
                ("r", "recover_instance", "Recover"),
                ("!", "purge_all", "Purge ALL"),
                ("/", "refresh_table", "Refresh Table"),
                ("s", "shell_into", "Shell"),               
                ("q", "quit", "QUIT")
                ]

    def compose(self) -> ComposeResult:
        """Create child widgets for the app."""
        yield Header()
        yield DataTable(cursor_type="row", id="datatable")
        yield RichLog()
        # yield Terminal(id="terminal_bash")
        yield Footer()

    def action_get_help(self) -> None:
        value = self.push_screen(HelpScreen())
        self.notify(f"Help Screen: {value}")
        # self.query_one(RichLog).write(value)

    def refresh_table(self) -> None:
        rows = get_instances_for_textual_datatable()
        table = self.query_one(DataTable)
        table = table.clear(columns=True)
        table.add_columns(*rows[0])
        table.add_rows(rows[1:])

    def get_selected_instance_name(self) -> str:
        table = self.query_one(DataTable)
        value = table.get_row_at(table.cursor_row)
        # Name has to 'always' be 0 column
        instance_name = value[0]
        return instance_name

    def on_mount(self) -> None:
        self.refresh_table()
        # terminal_bash: Terminal = self.query_one("#terminal_bash")
        # terminal_bash.start()

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

    def action_delete_instance(self) -> None:
        """An action to delete the selected instances"""
        instance_name = self.get_selected_instance_name()
        self.notify(f"Deleted {instance_name}")
        delete_instance(instance_name)
        self.refresh_table()

    def action_recover_instance(self) -> None:
        """An action to rescover the selected instances"""
        instance_name = self.get_selected_instance_name()
        self.notify(f"Recovered {instance_name}")
        recover_instance(instance_name)
        self.refresh_table()

    def action_quick_create_instance(self) -> None:
        """An action to quickly create an instance"""
        self.notify(f"Creating Instance")
        quick_create_instance()
        self.refresh_table()

    def action_purge_all(self) -> None:
        """An action to purge all instances"""
        self.notify(f"Purged All Instances")
        purge_instances()
        self.refresh_table()

    def action_shell_into(self) -> None:
        """An action to shell into the selected instances"""
        instance_name = self.get_selected_instance_name()
        self.notify(f"Shelling into {instance_name}")
        # shell_into(instance_name)

    def action_quit(self):
        self.exit()


def get_args():
    """ Get passed args """
    parser = argparse.ArgumentParser(description='Get Help')
    parser.add_argument('-h', '--help', metavar='help',
                        default='Runs a Text Interface for Multipass',
                        help='Info on this util')
    return parser.parse_args()


def main():
    """ Execute program """

    log("*** Program Started ***")
    mp_version = get_multipass_version()
    print(f"MP Version is: {mp_version}")
    print("*** Program Ended ***")
    #-----------------------------------------------------
    app = mptui()
    app.run()
    #-----------------------------------------------------

if __name__ == '__main__':
    main()
