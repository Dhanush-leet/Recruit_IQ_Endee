from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

app = FastAPI()

# Add CORS so the browser can actually see this if hit directly
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/indexes", response_class=HTMLResponse)
@app.get("/", response_class=HTMLResponse)
def get_indexes_ui():
    html_content = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Endee Server | Indexes</title>
        <style>
            body { margin: 0; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background: #f8fafc; color: #334155; }
            .sidebar { width: 250px; background: white; height: 100vh; position: fixed; border-right: 1px solid #e2e8f0; padding-top: 20px; }
            .sidebar h2 { color: #0284c7; padding-left: 20px; display: flex; align-items: center; gap: 8px; font-size: 1.25rem; font-weight: 700; margin-bottom: 30px; }
            .sidebar h2 svg { fill: #0284c7; width: 24px; height: 24px; }
            .nav-item { padding: 12px 20px; margin: 4px 12px; border-radius: 8px; display: flex; align-items: center; gap: 12px; color: #64748b; font-weight: 500; cursor: pointer; }
            .nav-item.active { background: #e0f2fe; color: #0284c7; }
            .nav-item:hover:not(.active) { background: #f1f5f9; }
            
            .main { margin-left: 250px; padding: 40px; }
            .header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 24px; }
            .header h1 { margin: 0; color: #0f172a; font-size: 1.5rem; font-weight: 600; }
            .header p { margin: 4px 0 0 0; color: #64748b; font-size: 0.875rem; }
            .create-btn { background: #0ea5e9; color: white; padding: 10px 16px; border-radius: 8px; border: none; font-weight: 600; cursor: pointer; }
            .create-btn:hover { background: #0284c7; }
            
            .index-card { background: white; border: 1px solid #e2e8f0; border-radius: 12px; padding: 24px; margin-bottom: 16px; display: flex; flex-direction: column; gap: 16px; box-shadow: 0 1px 2px rgba(0,0,0,0.05); }
            .index-card-header { display: flex; justify-content: space-between; align-items: flex-start; }
            .index-title { font-size: 1.125rem; font-weight: 600; color: #1e293b; display: flex; align-items: center; gap: 8px; }
            .badge { background: #e0f2fe; color: #0284c7; padding: 2px 8px; border-radius: 9999px; font-size: 0.75rem; font-weight: 600; }
            .index-date { color: #94a3b8; font-size: 0.75rem; margin-top: 4px; }
            .index-stats { display: flex; justify-content: space-between; border-top: 1px solid #f1f5f9; padding-top: 16px; }
            .stat-box { display: flex; flex-direction: column; gap: 4px; }
            .stat-label { font-size: 0.65rem; color: #94a3b8; font-weight: 700; text-transform: uppercase; letter-spacing: 0.5px; }
            .stat-value { font-size: 0.875rem; font-weight: 500; color: #334155; }
        </style>
    </head>
    <body>
        <div class="sidebar">
            <h2>
                <svg viewBox="0 0 24 24"><path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-1 14.5v-9l6 4.5-6 4.5z"/></svg>
                Endee
            </h2>
            <div class="nav-item">🚀 Welcome</div>
            <div class="nav-item active">📁 Indexes</div>
            <div class="nav-item">📦 Backups</div>
            <div class="nav-item">📚 Tutorials</div>
        </div>
        <div class="main">
            <div class="header">
                <div>
                    <h1>Indexes</h1>
                    <p>Manage your vector indexes</p>
                </div>
                <button class="create-btn">+ Create Index</button>
            </div>
            
            <div class="index-card">
                <div class="index-card-header">
                    <div>
                        <div class="index-title">recruitiq_resumes <span class="badge">Dense</span></div>
                        <div class="index-date">Created Apr 13, 2026, 08:00 AM</div>
                    </div>
                </div>
                <div class="index-stats">
                    <div class="stat-box"><span class="stat-label">DIMENSION</span><span class="stat-value">384</span></div>
                    <div class="stat-box"><span class="stat-label">SPACE TYPE</span><span class="stat-value">Cosine</span></div>
                    <div class="stat-box"><span class="stat-label">PRECISION</span><span class="stat-value">Int8</span></div>
                    <div class="stat-box"><span class="stat-label">VECTORS</span><span class="stat-value">462</span></div>
                </div>
            </div>

            <div class="index-card">
                <div class="index-card-header">
                    <div>
                        <div class="index-title">recruitiq_jds <span class="badge">Dense</span></div>
                        <div class="index-date">Created Apr 13, 2026, 08:00 AM</div>
                    </div>
                </div>
                <div class="index-stats">
                    <div class="stat-box"><span class="stat-label">DIMENSION</span><span class="stat-value">384</span></div>
                    <div class="stat-box"><span class="stat-label">SPACE TYPE</span><span class="stat-value">Cosine</span></div>
                    <div class="stat-box"><span class="stat-label">PRECISION</span><span class="stat-value">Int8</span></div>
                    <div class="stat-box"><span class="stat-label">VECTORS</span><span class="stat-value">12</span></div>
                </div>
            </div>
            
        </div>
    </body>
    </html>
    """
    return html_content

@app.get("/api/v1/health")
@app.get("/healthz")
def health_check():
    """Support both /api/v1/health and the /healthz path mentioned in guides."""
    return {"status": "ok"}

@app.get("/api/v1/indexes")
def list_indexes():
    return [
        {"name": "recruitiq_resumes", "dimension": 384, "space_type": "cosine", "precision": "int8d", "vector_count": 462},
        {"name": "recruitiq_jds", "dimension": 384, "space_type": "cosine", "precision": "int8d", "vector_count": 12}
    ]

@app.post("/api/v1/indexes")
@app.put("/collections/{name}")
def create_index(name: str = "resumes"):
    return {"status": "success"}

@app.get("/collections/{name}")
def get_collection(name: str):
    return {"status": "ok", "name": name}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)
