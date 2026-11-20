TOOLS = {
    "calculator": {"description": "Add, subtract, multiply, divide", "params": {"a": "number", "b": "number", "op": "string"}, "required": ["a", "b", "op"], "permission": "basic"},
    "search_docs": {"description": "Search docs by query", "params": {"query": "string"}, "required": ["query"], "permission": "basic"},
    "get_weather": {"description": "Get weather for city", "params": {"city": "string"}, "required": ["city"], "permission": "basic"},
    "send_email": {"description": "Send email - needs approval", "params": {"to": "string", "subject": "string", "body": "string"}, "required": ["to", "subject", "body"], "permission": "email"},
    "delete_file": {"description": "Delete file - admin only", "params": {"path": "string"}, "required": ["path"], "permission": "admin"},
}
AGENTS = {
    "helper": {"permissions": ["basic"], "description": "Basic helper - calculator, search, weather only"},
    "assistant": {"permissions": ["basic", "email"], "description": "Assistant - basic + email"},
    "admin": {"permissions": ["basic", "email", "admin"], "description": "Admin - all tools"},
}
DOCS = ["Python functions guide", "FastAPI tutorial", "React hooks guide", "Docker containers guide"]
HISTORY = []
def validate(tool_name, args):
    if tool_name not in TOOLS:
        return False, f"Tool '{tool_name}' is NOT registered. Available: {', '.join(TOOLS.keys())}"
    tool = TOOLS[tool_name]
    for req in tool["required"]:
        if req not in args:
            return False, f"Missing required argument: '{req}' for tool '{tool_name}'"
    for k, v in args.items():
        if k not in tool["params"]:
            return False, f"Unknown argument: '{k}' for tool '{tool_name}'"
        expected = tool["params"][k]
        if expected == "number" and not isinstance(v, (int, float)):
            return False, f"Invalid type for '{k}': expected number, got {type(v).__name__}"
        if expected == "string" and not isinstance(v, str):
            return False, f"Invalid type for '{k}': expected string, got {type(v).__name__}"
    return True, "Valid"
def execute(tool_name, args, agent="helper"):
    if agent not in AGENTS:
        result = {"success": False, "error": f"Unknown agent '{agent}'"}
        HISTORY.append({"agent": agent, "tool": tool_name, "args": args, "success": False, "result": result})
        return result
    valid, msg = validate(tool_name, args)
    if not valid:
        result = {"success": False, "error": msg}
        HISTORY.append({"agent": agent, "tool": tool_name, "args": args, "success": False, "result": result})
        return result
    perm = TOOLS[tool_name]["permission"]
    if perm not in AGENTS[agent]["permissions"]:
        result = {"success": False, "error": f"Permission denied: agent '{agent}' lacks '{perm}' permission for '{tool_name}'"}
        HISTORY.append({"agent": agent, "tool": tool_name, "args": args, "success": False, "result": result})
        return result
    try:
        if tool_name == "calculator":
            a, b, op = args["a"], args["b"], args["op"]
            out = {"add": a + b, "subtract": a - b, "multiply": a * b, "divide": a / b if b != 0 else "Error: divide by zero"}.get(op, f"Unknown op {op}")
        elif tool_name == "search_docs":
            q = args["query"].lower()
            out = [d for d in DOCS if q in d.lower()] or ["No docs found"]
        elif tool_name == "get_weather":
            out = f"Weather in {args['city']}: Sunny, 24C (mock)"
        elif tool_name == "send_email":
            out = f"Email sent to {args['to']}: {args['subject']}"
        elif tool_name == "delete_file":
            out = f"File {args['path']} deleted (mock - no real file touched)"
        else:
            out = "Unknown tool"
    except Exception as e:
        result = {"success": False, "error": f"Execution failed: {e}"}
        HISTORY.append({"agent": agent, "tool": tool_name, "args": args, "success": False, "result": result})
        return result
    result = {"success": True, "tool": tool_name, "output": out, "validated": True}
    HISTORY.append({"agent": agent, "tool": tool_name, "args": args, "success": True, "result": result})
    return result
def run_task(task: str, agent="helper", max_retries=2):
    steps = []
    low = task.lower()
    # Rule-based agent: plan steps from task keywords
    if "calculate" in low or "add" in low or "plus" in low:
        steps.append(("calculator", {"a": 10, "b": 5, "op": "add"}))
    if "weather" in low:
        steps.append(("get_weather", {"city": "Nairobi"}))
    if "search" in low or "docs" in low or "python" in low:
        steps.append(("search_docs", {"query": "python"}))
    if "email" in low:
        steps.append(("send_email", {"to": "test@example.com", "subject": "Task done", "body": "Hello"}))
    if not steps:
        steps.append(("search_docs", {"query": task}))
    results = []
    for tool_name, args in steps:
        attempt = 0
        while attempt <= max_retries:
            r = execute(tool_name, args, agent)
            results.append({"tool": tool_name, "args": args, "attempt": attempt + 1, **r})
            if r["success"]:
                break
            attempt += 1
    completed = sum(1 for r in results if r["success"])
    return {"task": task, "agent": agent, "steps": results, "completed": completed, "total": len(results), "score": round(completed / max(len(results), 1) * 100, 1), "success": completed == len(results)}