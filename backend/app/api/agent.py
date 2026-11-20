from fastapi import APIRouter
from pydantic import BaseModel
from typing import Dict, Any
from ..services.tools import TOOLS, AGENTS, HISTORY, execute, run_task, validate
router = APIRouter()
class CallIn(BaseModel):
    tool: str
    args: Dict[str, Any] = {}
    agent: str = "helper"
class TaskIn(BaseModel):
    task: str
    agent: str = "helper"
@router.get("/tools")
def tools():
    return {"total": len(TOOLS), "tools": TOOLS, "agents": AGENTS}
@router.post("/call")
def call(body: CallIn):
    return execute(body.tool, body.args, body.agent)
@router.post("/task")
def task(body: TaskIn):
    return run_task(body.task, body.agent)
@router.get("/history")
def history():
    return {"total": len(HISTORY), "history": HISTORY}
@router.post("/replay")
def replay():
    replayed = []
    for h in HISTORY:
        r = execute(h["tool"], h["args"], h["agent"])
        replayed.append({"tool": h["tool"], "args": h["args"], "replayed_success": r["success"]})
    return {"total": len(replayed), "replayed": replayed}
@router.get("/evaluation")
def evaluation():
    total = len(HISTORY)
    passed = sum(1 for h in HISTORY if h["success"])
    failed = total - passed
    return {"total_calls": total, "passed": passed, "failed": failed, "success_rate": round(passed / max(total, 1) * 100, 1), "blocked_unregistered": sum(1 for h in HISTORY if not h["success"] and "NOT registered" in str(h["result"].get("error", ""))), "blocked_permission": sum(1 for h in HISTORY if not h["success"] and "Permission denied" in str(h["result"].get("error", "")))}