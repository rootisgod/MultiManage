import subprocess
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
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

@app.get("/")
def list_instances():
    return multipass_functions.multipass_version()

@app.get("/list")
def list_instances():
    return multipass_functions.list_multipass_instances()

@app.get("/version")
def list_instances():
    return multipass_functions.multipass_version()