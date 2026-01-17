from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from contextlib import asynccontextmanager
import os

from .database import create_db_and_tables
from .routers import api

@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield

app = FastAPI(lifespan=lifespan)

app.include_router(api.router)

# Serve static files
# We mount the 'frontend' directory to serve CSS, JS, etc.
# Ideally, we should serve index.html for root, public.html and private.html for correct paths
# But for simplicity, we map / -> index.html, /p/{id} -> public.html, /r/{id} -> private.html

# Ensure backend can find frontend relative to CWD or file location
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FRONTEND_DIR = os.path.join(BASE_DIR, "frontend")

app.mount("/static", StaticFiles(directory=FRONTEND_DIR), name="static")

@app.get("/")
async def read_index():
    return FileResponse(os.path.join(FRONTEND_DIR, "index.html"))

@app.get("/p/{public_id}")
async def read_public_page(public_id: str):
    # Just serve the HTML, JS will handle fetching data by ID
    return FileResponse(os.path.join(FRONTEND_DIR, "public.html"))

@app.get("/r/{private_id}")
async def read_private_page(private_id: str):
    # Just serve the HTML, JS will handle fetching data by ID
    return FileResponse(os.path.join(FRONTEND_DIR, "private.html"))
