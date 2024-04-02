import yaml
import subprocess
import json
from textual.app import App
from textual.widgets import DataTable
from textual.scroll_view import ScrollView
from rich.text import Text

cmd = 'multipass find --format json'
result = subprocess.run(cmd.split(), capture_output=True, text=True)
print(result.stdout)

# Run the multipass list command and capture the output
try:
    output = subprocess.check_output(['multipass', 'list', '--format', 'json'])
except subprocess.CalledProcessError as e:
    print(f"Error executing multipass command: {e}")
    exit(1)

headers = ['Name', 'State', 'IPv4', 'Release']
instances = json.loads(output)['list']

# Extract the relevant information from each instance
data = []
for instance in instances:
    name = instance['name']
    state = instance['state']
    ipv4 = instance.get('ipv4', [''])[0]  # Get the first IPv4 address or an empty string
    release = instance['release']
    data.append([name, state, ipv4, release])
print(data)

# --------------------------------------------------------------------------------

# Column headers
headers = ['Name', 'State', 'IPv4', 'Release']

# Row data
row_data = ['profitable-protozoa', 'Running', 'kjhkhjkjh', 'Ubuntu 22.04 LTS']

class TableExample(App):
    async def on_mount(self, event):
        # Create a table widget
        table = DataTable(show_cursor=True)

        # Add columns to the table
        table.add_columns(*headers)

        # Add rows to the table
        table.add_row(*[Text(str(cell)) for cell in row_data])

        # Create a scroll view and add the table to it
        scroll_view = ScrollView(table)

        # Add the scroll view to the app
        await self.bind(scroll_view, "app")

app = TableExample()
app.run()