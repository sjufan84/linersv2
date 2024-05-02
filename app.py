""" This module contains the FastAPI application. It's responsible for
    creating the FastAPI application and including the routers."""
from fastapi import FastAPI
# Import routers
from routes.clone_routes import router as clone_routes
from fastapi.middleware.cors import CORSMiddleware

DESCRIPTION = """
# LinerGen FastAPI

## Project Overview

## Functionality

LinerGenV1 FastAPI supports:

## Dependencies

## Installation

To install these dependencies, use 'pip', the Python package installer:

```python
pip install -r requirements.txt
"""

app = FastAPI(
    title="LinerGenV2",
    description=DESCRIPTION,
    version="0.1",
    summary="Backend for vocal cloning related to the linerGen project",
    contact={
        "name": "Dave Thomas",
        "url": "https://enoughwebapp.com",
        "email": "dave_thomas@enoughwebapp.com"
    },
    license_info={
        "name": "MIT License",
        "url": "https://opensource.org/licenses/MIT"
    }
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Include routers
routers = [clone_routes]
for router in routers:
    app.include_router(router)
