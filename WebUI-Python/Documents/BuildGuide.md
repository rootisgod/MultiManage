# MultiManage
WebUI (and potentially TUI) to manage multipass.

To document here... Going for a set of functions and can then split the program into a WebUI and TUI version

Can't use multipass with docker easily so do python and npm seperately

## Python

```bash
# Pre-reqs
python3 -m venv venv
. ./venv/bin/activate
pip install -r requirements.txt
```

## Running

Ensure taskfile is installed

```bash
task start-all
```