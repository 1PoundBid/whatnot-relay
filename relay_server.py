import os
import time
from fastapi import FastAPI, Header, HTTPException
from fastapi.middleware.cors import CORSMiddleware

APP_TOKEN = os.environ.get("APP_TOKEN", "CHANGE_ME")

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/health")
def health():
    return {"ok": True, "ts": time.time()}

@app.get("/api/printers")
def printers(x_app_token: str = Header(default="")):
    if x_app_token != APP_TOKEN:
        raise HTTPException(status_code=401, detail="bad token")
    return {"printers": []}
