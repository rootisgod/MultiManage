#!/usr/bin/env python3
"""
Author:  Iain
Purpose: Multipass TU
"""

import argparse
import subprocess
import re
import json
from typing import Dict, Any


def get_args():
    """ Get passed args """

    parser = argparse.ArgumentParser(description='Get Help')
    parser.add_argument('-h', '--help', metavar='help',
                        default='Runs a Text Interface for Multipass',
                        help='Info on this util')
    return parser.parse_args()


def run_multipass_command(command):
    """
    Run a multipass command and capture its output.

    Args:
        command (str): The command to run.

    Returns:
        str: The output of the command.
    """
    try:
        # Run the command and capture its output
        result = subprocess.run(command, shell=True, check=True,
                                capture_output=True, text=True)
        output = result.stdout.strip()
        return output
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")
        return None


def get_multipass_version() -> str:
    """
    Check we can see multipass and get its version

    Returns:
        str: The multipass version number we are running

    """
    try:
        output = run_multipass_command('multipass --version')
        lines = output.splitlines()
        pattern = r'\b\d+\.\d+\.\d+'
        match = re.search(pattern, lines[0])
        if match:
            version = match.group()
        else:
            version = None
        output = version
        return output
    except subprocess.CalledProcessError as e:
        print(f"Error executing multipass command: {e}")
        exit(1)


def get_multipass_instances() -> Dict[str, Any]:
    """
    Get a json object of all instances

        Returns:
        Dict: An object that has the multipass instances in JSON/DICT format

    """
    try:
        output = run_multipass_command('multipass list --format json')
        instances = json.loads(output)
        # Check if the "list" key contains any items
        if len(instances["list"]) >= 0:
            return instances
        else:
            return None
    except Exception as e:
        # Handle any exceptions gracefully
        print(f"An error occurred getting the instances: {e}")
        return None


def change_multipass_instance_power_state(instance_name: str, desired_state: str):
    """
    Start, stop, or suspend a multipass instance

    Args:
        instance_name (str): The name of the instance to start.
        desired_state (str): The state to make the instance

    """
    allowed_states = ['start', 'stop', 'suspend']
    if desired_state in allowed_states:
        try:
            run_multipass_command(f'multipass {desired_state} {instance_name}')
        except Exception as e:
            # Handle any exceptions gracefully
            print(f"An error occurred getting the instances: {e}")
            return None
    else:
        print(f"Can only {allowed_states} instances")


def get_running_multipass_instance_names() -> list[str, Any]:
    """ Return names of running instances """

    instances = get_multipass_instances()
    running_instance_names = [item['name'] for item in instances['list']
                              if item['state'] == 'Running']
    return running_instance_names


def get_stopped_multipass_instance_names() -> list[str, Any]:
    """ Return names of stopped instances """

    instances = get_multipass_instances()
    stopped_instance_names = [item['name'] for item in instances['list']
                              if item['state'] == 'Stopped']
    return stopped_instance_names


def get_suspended_multipass_instance_names() -> list[str, Any]:
    """ Return names of suspended instances """

    instances = get_multipass_instances()
    suspended_instance_names = [item['name'] for item in instances['list']
                              if item['state'] == 'Suspended']
    return suspended_instance_names


def get_stopped_multipass_instances() -> Dict[str, Any]:
    """ Return stopped instances """

    instances = get_multipass_instances()
    stopped_instances = [item for item in instances['list']
                         if item['state'] == 'Stopped']
    return stopped_instances


def get_suspended_multipass_instances() -> Dict[str, Any]:
    """ Return suspended instances """

    instances = get_multipass_instances()
    suspended_instances = [item for item in instances['list']
                         if item['state'] == 'Suspended']
    return suspended_instances


def get_running_multipass_instances() -> Dict[str, Any]:
    """ Return running instances """

    instances = get_multipass_instances()
    running_instances = [item for item in instances['list']
                         if item['state'] == 'Running']
    return running_instances


def stop_instance(name: str) -> bool:
    """ Stop an instance """

    print("stop_instance")


def main():
    """ Execute program """

    print("*** Program Started ***")
    mp_version = get_multipass_version()
    print(f"MP Version is: {mp_version}")
    print("*** Program Ended ***")


if __name__ == '__main__':
    main()
