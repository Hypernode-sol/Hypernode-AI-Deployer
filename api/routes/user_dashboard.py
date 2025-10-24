from __future__ import annotations
from fastapi import APIRouter, Response
from ...core.job_scheduler import JobScheduler
from ...core.model_registry import ModelRegistry

router = APIRouter(tags=["dashboard"])

_registry = ModelRegistry()
_scheduler = JobScheduler(_registry)


DASHBOARD_HTML = """
<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>Hypernode AI Dashboard</title>
    <style>
      body{font-family:system-ui,-apple-system,Segoe UI,Roboto,Ubuntu,Helvetica,Arial,sans-serif;margin:2rem;color:#e5e7eb;background:#0b0f19}
      h1{font-size:1.5rem;margin:0 0 1rem}
      .card{background:#0f172a;border:1px solid #1f2937;border-radius:14px;padding:1rem;margin-bottom:1rem}
      .row{display:flex;gap:1rem;flex-wrap:wrap}
      .pill{font-size:.8rem;border:1px solid #374151;padding:.2rem .5rem;border-radius:999px}
      table{width:100%;border-collapse:collapse}
      th,td{padding:.5rem;border-bottom:1px solid #1f2937;text-align:left}
      .muted{color:#9ca3af}
    </style>
  </head>
  <body>
    <h1>Hypernode AI Dashboard</h1>
    <div class="row">
      <div class="card"><div class="pill">Models</div><div id="models"></div></div>
      <div class="card" style="flex:1 1 480px">
        <div class="pill">Jobs</div>
        <table id="jobs"><thead><tr><th>ID</th><th>Status</th><th>Progress</th><th>Message</th></tr></thead><tbody></tbody></table>
        <div class="muted">Auto-refresh every 2s</div>
      </div>
    </div>
    <script>
      async function loadModels(){
        const res = await fetch('/api/list_models');
        const data = await res.json();
        const root = document.getElementById('models');
        root.innerHTML = data.map(m => `<div>${m.name} <span class='pill'>${m.task}</span></div>`).join('');
      }
      async function loadJobs(){
        // Simplified: there is no list endpoint; we probe a known set of job IDs in a real app.
        // This placeholder keeps the UI minimal.
      }
      setInterval(loadJobs, 2000);
      loadModels();
    </script>
  </body>
</html>
"""


@router.get("/user_dashboard")
def user_dashboard() -> Response:
    """Return a minimal HTML dashboard (static) for demo purposes."""
    return Response(content=DASHBOARD_HTML, media_type="text/html")

