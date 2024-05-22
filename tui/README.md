# Testing

# TODO
- Add a way to get vm name in selected cell to start/stop selected vm
- Create a banner/popup progress screen when a long running operation is happening (ie starting a VM)
  https://textual.textualize.io/guide/widgets/
- Add more items like start/stop/suspend/delete/purge/snapshot/enter_shell
- Add popup screen if easy for things like;
  - Create instance
  - Create snapshot
  - Revert Snapshot
  - etc

# Good Examples

https://github.com/charles-001/dolphie

# Quick Test

Just runs against existing multipass setup, make or taskfile (https://taskfile.dev/installation/)

```bash
make test
task test
```

## Full Test

This will created multipass instances and test various number of instances etc...

Will delete all existing instances!

```bash
make full-test
task full-test
```

## Other

Just nice quality of life ones

```bash
make create-test-instances
make delete-all-instances

test create-test-instances
test delete-all-instances
```


# Build

To build a binary, do this.

## MAC
```
pip install pyinstaller
pyinstaller -F -w -n mptui main.py
./dist/mptui
```


# Textualize

Some basic notes

## The general thing

https://textual.textualize.io/guide/app/

You start from an app class

```python
from textual.app import App

class MyApp(App):
    pass

if __name__ == "__main__":
    app = MyApp()
    app.run()
```

Then, you can have an on_mount() command. The mount event is sent immediately after entering application mode.

```python
    def on_mount(self) -> None:
        self.screen.styles.background = "darkblue"
```

Widgets are self-contained components responsible for generating the output for a portion of the screen.
Widgets can be as simple as a piece of text, a button, or a fully-fledged component like a text editor or file browser (which may contain widgets of their own).

To add widgets to your app implement a compose() method which should return an iterable of Widget instances. A list would work, but it is convenient to yield widgets, making the method a generator.

The following example imports a builtin Welcome widget and yields it from App.compose().
When you run this code, Textual will mount the Welcome widget which contains Markdown content and a button:

```python
from textual.app import App, ComposeResult
from textual.widgets import Welcome

class WelcomeApp(App):
    def compose(self) -> ComposeResult:
        yield Welcome()

    def on_button_pressed(self) -> None:
        self.exit()
        
if __name__ == "__main__":
  app = WelcomeApp()
  app.run()
```

While composing is the preferred way of adding widgets when your app starts it is sometimes necessary to add new widget(s) in response to events. You can do this by calling mount() which will add a new widget to the UI.

```python
class WelcomeApp(App):
    def on_key(self) -> None:
        self.mount(Welcome())

    def on_button_pressed(self) -> None:
        self.exit()
```

When you mount a widget, Textual will mount everything the widget composes. Textual guarantees that the mounting will be complete by the next message handler, but not immediately after the call to mount(). This may be a problem if you want to make any changes to the widget in the same message handler.

```python
class WelcomeApp(App):
    async def on_key(self) -> None:
        await self.mount(Welcome())
        self.query_one(Button).label = "YES!"
```

