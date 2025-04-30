import subprocess
from fastapi import FastAPI, Body
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import multipass_functions

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Replace "*" with specific origins like ["http://localhost:3000"] for better security
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class InstanceRequest(BaseModel):
    name: str

@app.get("/")
def list_instances():
    return multipass_functions.multipass_version()

@app.get("/list")
def list_instances():
    return multipass_functions.list_multipass_instances()

@app.get("/version")
def list_instances():
    return multipass_functions.multipass_version()

@app.get("/debug/list")
def debug_list_instances():
    """
    Endpoint for debugging the list instances function
    """
    raw_result = multipass_functions.list_multipass_instances()
    return {
        "raw_result": raw_result,
        "has_list_key": "list" in raw_result,
        "structure": str(type(raw_result)),
        "keys": list(raw_result.keys()) if isinstance(raw_result, dict) else "Not a dict"
    }
