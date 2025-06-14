import subprocess
import json

def run_multipass_command(command, expect_json=True):
    """
    Run a multipass command and capture its output.

    Args:
        command (str): The command to run.
        expect_json (bool): Whether to parse the output as JSON.

    Returns:
        dict or str: The output of the command, parsed as JSON if expect_json=True.
    """
    try:
        # Run the command and capture its output
        result = subprocess.run(command, shell=True, check=True,
                                capture_output=True, text=True)
        output = result.stdout.strip()
        
        if expect_json:
            try:
                return json.loads(output)
            except json.JSONDecodeError:
                return {"message": output}
        else:
            return {"message": output}
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")
        return {"error": str(e), "stderr": e.stderr}

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
    result = run_multipass_command('multipass list --format json')
    return result
    
def stop_multipass_instance(name):
    """
    Calls 'multipass stop' and returns the result.
    
    Args:
        name (str): The name of the instance to stop.
        
    Returns:
        dict: The result of the command execution.
    """
    result = run_multipass_command(f'multipass stop {name}', expect_json=False)
    return result

def start_multipass_instance(name):
    """
    Calls 'multipass start' and returns the result.
    
    Args:
        name (str): The name of the instance to start.
        
    Returns:
        dict: The result of the command execution.
    """
    result = run_multipass_command(f'multipass start {name}', expect_json=False)
    return result


def get_multipass_instance_info(name):
    """
    Calls 'multipass info' and returns the output or error.
    
    Args:
        name (str): The name of the instance to get info about.
        
    Returns:
        dict: The result of the command execution.
    """
    result = run_multipass_command(f'multipass info {name} --format json')
    return result