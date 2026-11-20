import { useState, useEffect } from "react";
const API = "http://127.0.0.1:8006/api";
export default function App() {
  const [tools, setTools] = useState({});
  const [agents, setAgents] = useState({});
  const [agent, setAgent] = useState("helper");
  const [tool, setTool] = useState("calculator");
  const [argsText, setArgsText] = useState('{"a":10,"b":5,"op":"add"}');
  const [task, setTask] = useState("calculate and check weather");
  const [result, setResult] = useState(null);
  const [taskResult, setTaskResult] = useState(null);
  const [history, setHistory] = useState([]);
  const [evalData, setEvalData] = useState(null);
  const loadTools = async () => { const r = await fetch(`${API}/tools`); const d = await r.json(); setTools(d.tools); setAgents(d.agents); };
  const loadHistory = async () => { const r = await fetch(`${API}/history`); setHistory((await r.json()).history); };
  useEffect(() => { loadTools(); loadHistory(); }, []);
  const callTool = async () => { let args = {}; try { args = JSON.parse(argsText); } catch { setResult({ success: false, error: "Invalid JSON in args" }); return; } const r = await fetch(`${API}/call`, { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({ tool, args, agent }) }); setResult(await r.json()); loadHistory(); };
  const runTask = async () => { const r = await fetch(`${API}/task`, { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({ task, agent }) }); setTaskResult(await r.json()); loadHistory(); };
  const getEval = async () => { const r = await fetch(`${API}/evaluation`); setEvalData(await r.json()); };
  const replay = async () => { const r = await fetch(`${API}/replay`, { method: "POST" }); setResult(await r.json()); };
  return (<div style={{ maxWidth: 900, margin: "auto", padding: 20, fontFamily: "sans-serif" }}>
    <h1>🤖 Agent Tool-Calling Simulation</h1>
    <p>Agents can ONLY call registered tools with validated args + authorized permissions.</p>
    <h3>Tool Registry</h3>{Object.entries(tools).map(([n, t]) => <div key={n} style={{ border: "1px solid #ddd", padding: 8, marginTop: 6 }}><b>{n}</b> - {t.description} | Params: {JSON.stringify(t.params)} | Permission: {t.permission}</div>)}
    <h3>Call A Tool</h3><select value={agent} onChange={e => setAgent(e.target.value)} style={{ padding: 10 }}>{Object.keys(agents).map(a => <option key={a} value={a}>{a} - {agents[a]?.description}</option>)}</select><select value={tool} onChange={e => setTool(e.target.value)} style={{ padding: 10, marginLeft: 8 }}>{Object.keys(tools).map(t => <option key={t} value={t}>{t}</option>)}</select>
    <input value={argsText} onChange={e => setArgsText(e.target.value)} style={{ width: "100%", padding: 10, marginTop: 8, fontFamily: "monospace" }} />
    <button onClick={callTool} style={{ padding: 10, marginTop: 8 }}>Call Tool</button>
    {result && <pre style={{ background: result.success === false ? "#ffe6e6" : "#e6ffe6", padding: 12, marginTop: 8 }}>{JSON.stringify(result, null, 2)}</pre>}
    <h3>Run Task</h3><input value={task} onChange={e => setTask(e.target.value)} style={{ width: "100%", padding: 10 }} /><button onClick={runTask} style={{ padding: 10, marginTop: 8 }}>Run Task</button><button onClick={getEval} style={{ padding: 10, marginLeft: 8 }}>Evaluation</button><button onClick={replay} style={{ padding: 10, marginLeft: 8 }}>Replay History</button>
    {evalData && <div style={{ background: "#eef", padding: 12, marginTop: 12 }}><b>Evaluation:</b> Total {evalData.total_calls} | Passed {evalData.passed} | Failed {evalData.failed} | Success {evalData.success_rate}% | Blocked Unregistered {evalData.blocked_unregistered} | Blocked Permission {evalData.blocked_permission}</div>}
    {taskResult && <div style={{ border: "2px solid #333", padding: 12, marginTop: 12 }}><h3>Task: {taskResult.task} - Score {taskResult.score}% | {taskResult.completed}/{taskResult.total}</h3>{taskResult.steps.map((s, i) => <div key={i} style={{ padding: 8, background: s.success ? "#e6ffe6" : "#ffe6e6", marginTop: 6 }}><b>{s.success ? "✅" : "❌"} {s.tool}</b> (attempt {s.attempt}) - {s.output || s.error}</div>)}</div>}
    <h3>Execution History ({history.length})</h3>{history.slice().reverse().map((h, i) => <div key={i} style={{ padding: 8, borderBottom: "1px solid #eee" }}><b>{h.success ? "✅" : "❌"} {h.agent} → {h.tool}</b> {JSON.stringify(h.args)} - {h.result.output || h.result.error}</div>)}
  </div>);
}