# MultiManage
WebUI (and potentially TUI) to manage multipass.

To document here... Going for a set of functions and can then split the program into a WebUI and TUI version

Can't use multipass with docker easily so do python and npm seperately

## Python

```bash
# Pre-rews
python3 -m venv venv
. ./venv/bin/activate
pip install -r requirements.txt
# Run in Background
uvicorn main:app --host 0.0.0.0 --port 8000 &
# Kill it
jobs
kill %1
```

Example URL
(http://localhost:8000/multipass/list)[http://localhost:8000/multipass/list]


## Next.js