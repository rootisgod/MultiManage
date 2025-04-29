import subprocess
from fastapi import FastAPI

app = FastAPI()

@app.get("/multipass/list")
def list_instances():
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