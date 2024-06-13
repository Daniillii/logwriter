from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from config.routers import RouterManager
from config.database import DatabaseManager
from config.tasks import TaskManager
from config.settings import MEDIA_DIR, ALLOWED_HOSTS

from apps.scheduler import scheduler

# -------------------
# --- Init Models ---
# -------------------

DatabaseManager().load()

# --------------------
# --- Init FastAPI ---
# --------------------

app = FastAPI()


TaskManager().import_tasks()


# ----------------------------
# --- Init FastAPI Events ----
# ----------------------------

@app.on_event("startup")
async def startup():
    scheduler.start()


@app.on_event("shutdown")
async def shutdown():
    scheduler.shutdown()


# ------------------
# --- Middleware ---
# ------------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_HOSTS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -------------------
# --- Static File ---
# -------------------

# add static-file support, for see images by URL
app.mount("/media", StaticFiles(directory=MEDIA_DIR), name="media")

# --------------------
# --- Init Routers ---
# --------------------

RouterManager(app).import_routers()
