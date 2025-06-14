import multipass_functions
from fastapi import APIRouter

router = APIRouter()

@router.get("/version")
def get_version():
    return multipass_functions.multipass_version()