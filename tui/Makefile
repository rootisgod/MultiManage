.PHONY: test

test:
	pytest -xvs test.py

full-test:
	multipass delete --all
	multipass purge
	pytest -xvs test.py
	multipass launch --name vm1
	pytest -xvs test.py
	multipass launch --name vm2
	pytest -xvs test.py
	multipass stop vm1
	pytest -xvs test.py
	multipass stop vm2
	pytest -xvs test.py
	multipass delete --all
	multipass purge
	pytest -xvs test.py

create-test-instances:
	multipass delete --all
	multipass purge
	multipass launch --name vm1
	multipass launch --name vm2

delete-all-instances:
	multipass delete --all
	multipass purge