from app.services.tools import execute, run_task, HISTORY
def test_valid_call():
    r = execute("calculator", {"a": 10, "b": 5, "op": "add"}, "helper")
    assert r["success"] is True and r["output"] == 15
def test_invalid_args():
    r = execute("calculator", {"a": "bad", "b": 5, "op": "add"}, "helper")
    assert r["success"] is False and "Invalid type" in r["error"]
def test_unavailable_tool():
    r = execute("hack_system", {}, "helper")
    assert r["success"] is False and "NOT registered" in r["error"]
def test_permission_failure():
    r = execute("send_email", {"to": "a@b.com", "subject": "hi", "body": "hi"}, "helper")
    assert r["success"] is False and "Permission denied" in r["error"]
def test_task_completion():
    r = run_task("calculate and check weather", "helper")
    assert r["success"] is True and r["score"] == 100.0