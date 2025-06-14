import multipass_functions
from fastapi import APIRouter

router = APIRouter()

@router.get("/list")
def list_instances():
    return multipass_functions.list_multipass_instances()