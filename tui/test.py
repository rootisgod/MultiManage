#!/usr/bin/env python3
"""tests for mptui.py"""

import os
import re
from mptui import *

prg = './mptui.py'


# --------------------------------------------------
def test_exists():
    """program exists"""

    assert os.path.isfile(prg)


def test_version():
    """program exists"""

    version = get_multipass_version()
    print(version)
    # Like 1.13.1
    pattern = r'\b\d+\.\d+\.\d+\b'
    match = re.search(pattern, version)
    assert match is not None


def test_get_multipass_instances():
    """Test that we can get a list of instance in multipass"""

    instances = get_multipass_instances()
    number_of_instances = len(instances["list"])
    print(f"We have { number_of_instances } instances")
    # To add 1, and many tests no, None works.
    assert number_of_instances >= 0


def test_get_multipass_instances_info():
    """Test that we can get all multipass instances"""

    instances = get_multipass_instances()
    print(instances)
    assert instances is not None


def test_get_running_multipass_instances():
    """Test that we can get a list of running instances in multipass"""

    instances = get_running_multipass_instances()
    number_of_instances = len(instances)
    print(f"We have { number_of_instances } running instances")
    # To add 1, and many tests no, None works.
    assert number_of_instances >= 0


def test_get_stopped_multipass_instances():
    """Test that we can get a list of stopped instances in multipass"""

    instances = get_stopped_multipass_instances()
    number_of_instances = len(instances)
    print(f"We have { number_of_instances } stopped instances")
    # To add 1, and many tests no, None works.
    assert number_of_instances >= 0


def test_get_suspended_multipass_instances():
    """Test that we can get a list of suspended instances in multipass"""

    instances = get_suspended_multipass_instances()
    number_of_instances = len(instances)
    print(f"We have { number_of_instances } suspended instances")
    # To add 1, and many tests no, None works.
    assert number_of_instances >= 0


def test_get_suspended_multipass_instance_names():
    """Test that we can get a list of suspended instances in multipass"""

    instances = get_suspended_multipass_instance_names()
    number_of_instances = len(instances)
    print(f"Suspended instances: { instances }")
    # To add 1, and many tests no, None works.
    assert number_of_instances >= 0


def test_get_stopped_multipass_instance_names():
    """Test that we can get a list of stopped instances in multipass"""

    instances = get_stopped_multipass_instance_names()
    number_of_instances = len(instances)
    print(f"Stopped instances: { instances }")
    # To add 1, and many tests no, None works.
    assert number_of_instances >= 0


def test_get_running_multipass_instance_names():
    """Test that we can get a list of running instances in multipass"""

    instances = get_running_multipass_instance_names()
    number_of_instances = len(instances)
    print(f"Running instances: { instances }")
    # To add 1, and many tests no, None works.
    assert number_of_instances >= 0


# TODO
# Assert I can get machines from multipass (0 *, 1 ,many)
# Assert I can get only ones running (0, 1 ,many)
# Assert I can get ones with snapshots (0, 1 ,many)
