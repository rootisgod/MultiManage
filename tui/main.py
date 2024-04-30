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
from textual.widgets import Header, Footer


# https://textual.textualize.io/tutorial/
class mptui(App):
    """A Textual app to manage multipass."""

    BINDINGS = [("d", "toggle_dark", "Toggle dark mode")]

    def compose(self) -> ComposeResult:
        """Create child widgets for the app."""
        yield Header()
        yield Footer()

    def action_toggle_dark(self) -> None:
        """An action to toggle dark mode."""
        self.dark = not self.dark


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
    app = mptui()
    app.run()


if __name__ == '__main__':
    main()
