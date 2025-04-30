import subprocess

def list_multipass_instances():
    """
    Calls 'multipass list' and returns the output or error.
    """
    try:
        result = subprocess.run(
            ["multipass", "list"],
            capture_output=True,
            text=True,
            check=True
        )
        return {"output": result.stdout}
    except subprocess.CalledProcessError as e:
        return {"error": e.stderr}