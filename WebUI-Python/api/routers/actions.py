import multipass_functions
from fastapi import APIRouter

router = APIRouter()

@router.get("/start/{name}")
def start_instance(name: str):
    """
    Start a multipass instance by name.
    """
    result = multipass_functions.start_multipass_instance(name)
    return result

@router.get("/stop/{name}")
def stop_instance(name: str):
    """
    Stop a multipass instance by name.
    """
    result = multipass_functions.stop_multipass_instance(name)
    return result

@router.get("/info/{name}")
def get_instance_info(name: str):
    """
    Get detailed information about a multipass instance.
    """
    result = multipass_functions.get_multipass_instance_info(name)
    return result
