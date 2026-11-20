from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.agent import router
app = FastAPI(title="Agent Tool-Calling Simulation")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])
app.include_router(router, prefix="/api")
@app.get("/api/health")
def health():
    return {"status": "ok", "engine": "registered-tools-only agent"}