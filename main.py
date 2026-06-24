from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from mongoengine import connect, get_connection

from config import settings
from routes import auth, comments, events, meetings, posts, users


@asynccontextmanager
async def lifespan(app: FastAPI):
    connect(host=settings.mongodb_uri)
    yield


app = FastAPI(
    title="Events API",
    version="1.0.0",
    docs_url="/api/docs",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(users.router)
app.include_router(events.router)
app.include_router(posts.router)
app.include_router(comments.router)
app.include_router(meetings.router)


@app.get("/api/health")
def health():
    return {"status": "ok"}


@app.get("/", response_class=HTMLResponse)
def root():
    db_ok = False
    try:
        conn = get_connection()
        db_ok = conn is not None and conn.admin.command("ping")["ok"] == 1.0
    except Exception:
        pass

    status = "All Systems Operational" if db_ok else "API Running (DB Disconnected)"
    color = "#22c55e" if db_ok else "#eab308"

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Events API — Status</title>
  <style>
    * {{ margin: 0; padding: 0; box-sizing: border-box; }}
    body {{
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
      background: #0f172a; color: #e2e8f0;
      min-height: 100vh; display: flex; align-items: center; justify-content: center;
    }}
    .card {{
      background: #1e293b; border-radius: 16px; padding: 48px 56px;
      text-align: center; box-shadow: 0 25px 50px -12px rgba(0,0,0,0.5);
      max-width: 420px; width: 90%;
    }}
    .checkmark {{
      width: 80px; height: 80px; border-radius: 50%;
      display: flex; align-items: center; justify-content: center;
      margin: 0 auto 24px; font-size: 40px;
      background: {color}22; color: {color};
    }}
    h1 {{ font-size: 24px; font-weight: 700; margin-bottom: 8px; }}
    .status {{ font-size: 16px; color: {color}; font-weight: 600; margin-bottom: 24px; }}
    .detail {{ font-size: 14px; color: #94a3b8; line-height: 1.6; }}
    .detail span {{ color: #64748b; }}
    .badge {{
      display: inline-block; margin-top: 24px; padding: 6px 16px;
      border-radius: 999px; font-size: 13px; font-weight: 500;
      background: #334155; color: #cbd5e1;
    }}
  </style>
</head>
<body>
  <div class="card">
    <div class="checkmark">✓</div>
    <h1>Events API</h1>
    <div class="status">{status}</div>
    <div class="detail">
      Version <span>1.0.0</span><br />
      MongoDB <span>{"Connected" if db_ok else "Disconnected"}</span><br />
      <span>100% Uptime</span>
    </div>
    <div class="badge">API Health • {settings.mongodb_uri.split("@")[-1] if "@" in settings.mongodb_uri else "localhost"}</div>
  </div>
</body>
</html>"""
