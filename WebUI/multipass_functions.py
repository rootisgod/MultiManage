import subprocess
import json

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
        result = result.stdout.strip()
        result = json.loads(result)
        return result
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")
        return None

def multipass_version():
    """
    Calls 'multipass version' and returns the output or error.
    """
    result = run_multipass_command('multipass version --format json')
    return result

def list_multipass_instances():
    """
    Calls 'multipass list' and returns the output or error.
    """
    # result = run_multipass_command('multipass list --format json')
    result = run_multipass_command('multipass list --format json')
    return result
    