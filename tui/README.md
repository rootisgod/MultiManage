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