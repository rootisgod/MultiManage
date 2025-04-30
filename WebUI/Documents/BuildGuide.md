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
```


## Next.js

Install Node

```bash
brew install node
npx create-next-app@latest multipass-web
cd multipass-web
npm install axios
```


## Running

Ensure taskfile is installed

```bash
task start-all
```