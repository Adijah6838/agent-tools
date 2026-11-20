# AI Agent Tool-Calling Simulation Framework
Controlled agent simulation. Agents can ONLY call registered tools with validated args + authorized permissions.
## Run Backend (Terminal 1)
cd backend; uvicorn app.main:app --port 8006 --reload
## Run Frontend (Terminal 2)
cd frontend; npm run dev
# http://localhost:5173/
## Test
cd backend; python -m pytest tests -v
## Tools
- calculator {a:number, b:number, op:string} - basic
- search_docs {query:string} - basic
- get_weather {city:string} - basic
- send_email {to, subject, body} - email
- delete_file {path:string} - admin
## Agents
- helper: basic only
- assistant: basic + email
- admin: all
## Endpoints
- GET /api/tools
- POST /api/call {tool, args, agent}
- POST /api/task {task, agent}
- GET /api/history
- POST /api/replay
- GET /api/evaluation
## Evaluation
Blocked unregistered + permission failures are counted. Task score = completed / total * 100.