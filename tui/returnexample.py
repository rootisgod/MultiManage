#!/usr/bin/env python3

# Hi all. Very sorry for such a noob question. But, i've got a main interface, and i'd like a 'popup' screen where I can present another screen with options, and that can then return values and I can perform an operation with the information. I'm pretty bad at coding, and i've likely got lots wrong here, but as a minimum viable program, I have a very basic example that creates a main screen, calls a class and creates an input box, and I cant figure out how to get that string info back to the main program. Would someone be kind enough to send me an existing example of what i'm trying to achieve, or show me what i'm doing wrong? (is this even the 'right' way) I'm not used to object orientated programming, so the message passing (and more!) is confusing me. But a single aha moment might be what i'm missing.

# Textual
from textual import on
from textual.app import App, ComposeResult
from textual.containers import Container
from textual.widgets import Footer, Input, Label, RichLog
from textual.screen import ModalScreen

class InputScreen(ModalScreen[None]):
    BINDINGS = [("escape", "pop_screen")]

    def compose(self) -> ComposeResult:
        with Container():
            yield Input()

    @on(Input.Submitted)
    def on_input_submitted(self):
        input = self.query_one(Input)
        return input.value

class input_popup(App):

    BINDINGS = [("i", "input_text", "Input Text")]        

    def compose(self) -> ComposeResult:
        yield Label()
        yield RichLog()
        yield Footer()

    def action_input_text(self) -> None:
        value = self.push_screen(InputScreen())
        # This fails: self.query_one(RichLog).log(f"Input Screen returned: {value}")

def main():
    app = input_popup()
    app.run()

if __name__ == '__main__':
    main()
