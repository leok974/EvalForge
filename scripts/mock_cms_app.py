import uvicorn
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import os

app = FastAPI(title="EvalForge Mock CMS")

# In-memory session-like state for deterministic testing
sessions = {}

@app.get("/healthz")
async def healthz():
    return {"status": "ok", "service": "evalforge-mock-cms"}

@app.get("/", response_class=HTMLResponse)
@app.get("/login", response_class=HTMLResponse)
async def login_page():
    return """
    <html>
        <head><title>CMS Login</title></head>
        <body>
            <h1>CMS Portal</h1>
            <form action="/login" method="post">
                <div>
                    <label>Username:</label>
                    <input type="text" name="username" data-testid="login-username" />
                </div>
                <div>
                    <label>Password:</label>
                    <input type="password" name="password" data-testid="login-password" />
                </div>
                <button type="submit" data-testid="login-submit">Login</button>
            </form>
        </body>
    </html>
    """

@app.post("/login", response_class=HTMLResponse)
async def login(username: str = Form(...), password: str = Form(...)):
    if username == "admin" and password == "secret123":
        return """
        <html>
            <head><title>Dashboard</title></head>
            <body>
                <h1 data-testid="dashboard-title">Welcome, Admin</h1>
                <p data-testid="core-status">Status: All systems operational.</p>
                <a href="/disputes" data-testid="nav-disputes">Manage Disputes</a>
            </body>
        </html>
        """
    else:
        return """
        <html>
            <body>
                <p style="color: red;" data-testid="login-error">Invalid credentials</p>
                <a href="/login">Try again</a>
            </body>
        </html>
        """

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
async def mock_login_basic():
    return await login_page()

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
    uvicorn.run(app, host="0.0.0.0", port=8765)
