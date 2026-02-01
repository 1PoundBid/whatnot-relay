
import os
import time
from fastapi import FastAPI, Header, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

APP_TOKEN = os.environ.get("APP_TOKEN")
AGENT_TOKEN = os.environ.get("AGENT_TOKEN")

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

cached_printers = []

class PrinterPayload(BaseModel):
    printers: list[str]

@app.get("/api/health")
def health():
    return {"ok": True}

@app.get("/api/printers")
def printers(x_app_token: str = Header(default="")):
    if x_app_token != APP_TOKEN:
        raise HTTPException(status_code=401, detail="bad token")
    return {"printers": cached_printers}

@app.post("/agent/printers")
def agent_printers(p: PrinterPayload, x_agent_token: str = Header(default="")):
    if x_agent_token != AGENT_TOKEN:
        raise HTTPException(status_code=401, detail="bad agent token")
    global cached_printers
    cached_printers = p.printers
    print("Printers updated:", cached_printers)
    return {"ok": True}
