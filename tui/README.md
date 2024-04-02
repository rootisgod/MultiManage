# Testing

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