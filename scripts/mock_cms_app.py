import uvicorn
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
import os

app = FastAPI(title="EvalForge Mock CMS")

# In-memory session-like state for deterministic testing
sessions = {}

# Resolve templates relative to this script so it works anywhere (host or Docker)
_HERE = os.path.dirname(os.path.abspath(__file__))
_TEMPLATES_DIR = os.environ.get(
    "MOCK_CMS_TEMPLATES_DIR",
    os.path.join(_HERE, "..", "data", "quests", "_shared", "mock_app", "templates")
)
templates = Jinja2Templates(directory=_TEMPLATES_DIR)

@app.get("/healthz")
async def healthz():
    return {"status": "ok", "service": "evalforge-mock-cms"}

@app.get("/", response_class=HTMLResponse)
@app.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.post("/login", response_class=HTMLResponse)
async def login(request: Request, username: str = Form(...), password: str = Form(...)):
    if username == "admin" and password == "secret123":
        return templates.TemplateResponse("dashboard.html", {"request": request})
    else:
        return templates.TemplateResponse("login.html", {"request": request, "error": "Invalid credentials"})

@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard(request: Request):
    return templates.TemplateResponse("dashboard.html", {"request": request})

@app.get("/latency", response_class=HTMLResponse)
async def latency(request: Request, delay: float = 3.0):
    return templates.TemplateResponse("latency.html", {"request": request, "delay": delay})

@app.get("/modals", response_class=HTMLResponse)
async def modals(request: Request):
    return templates.TemplateResponse("modals.html", {"request": request})

@app.get("/search", response_class=HTMLResponse)
async def search(request: Request, q: str = ""):
    return templates.TemplateResponse("search.html", {"request": request, "query": q})

@app.get("/disputes", response_class=HTMLResponse)
async def disputes():
    return """
    <html>
        <head><title>Disputes</title></head>
        <body>
            <h1>Active Disputes</h1>
            <table data-testid="results-table">
                <thead>
                    <tr><th>ID</th><th>Status</th><th>Action</th></tr>
                </thead>
                <tbody>
                    <tr data-testid="results-row-4712923">
                        <td>4712923</td>
                        <td>Pending</td>
                        <td><a href="/disputes/4712923" data-testid="view-4712923">View</a></td>
                    </tr>
                </tbody>
            </table>
        </body>
    </html>
    """

@app.get("/disputes/{dispute_id}", response_class=HTMLResponse)
async def dispute_detail(dispute_id: str):
    return f"""
    <html>
        <head><title>Dispute {dispute_id}</title></head>
        <body>
            <h1 data-testid="dispute-title">Dispute: {dispute_id}</h1>
            <div data-testid="dispute-detail-panel">
                <p>Amount: $1,200.00</p>
                <p>Reason: Unauthorized Transaction</p>
            </div>
            <button data-testid="dispute-resolve-btn">Resolve</button>
        </body>
    </html>
    """

# Mock fixtures for specific quest scenarios
@app.get("/mock/login-basic", response_class=HTMLResponse)
async def mock_login_basic(request: Request):
    return await login_page(request)

@app.get("/mock/activity-history", response_class=HTMLResponse)
async def mock_activity_history():
    return """
    <html>
        <body>
            <h1>System Activity</h1>
            <div data-testid="activity-history-panel">
                <ul>
                    <li>Login at 10:00 AM</li>
                    <li>Password changed at 10:05 AM</li>
                </ul>
            </div>
        </body>
    </html>
    """

if __name__ == "__main__":
    port = int(os.environ.get("MOCK_CMS_PORT", "8765"))
    uvicorn.run(app, host="0.0.0.0", port=port, log_level="info")
