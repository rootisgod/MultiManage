from fastapi import FastAPI, Body
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# Our Routers
from routers.info import router as info_router
from routers.list import router as list_router
from routers.version import router as version_router
from routers.actions import router as actions_router

# Main App
app = FastAPI()
app.include_router(info_router)
app.include_router(list_router)
app.include_router(version_router)
app.include_router(actions_router)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Replace "*" with specific origins like ["http://localhost:3000"] for better security
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def version():
    return "Hello from Multipass API!"
