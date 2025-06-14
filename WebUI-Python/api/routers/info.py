import multipass_functions
from fastapi import APIRouter

router = APIRouter()

@router.get("/instance/{name}")
def get_instance_info(name: str):
    return multipass_functions.get_multipass_instance_info(name)