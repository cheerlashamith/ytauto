from __future__ import annotations
import os
from pathlib import Path
from fastapi import FastAPI, HTTPException, Query, Body
from fastapi.responses import FileResponse, JSONResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles
from backend.core.config import project_root, get_config, save_config
from backend.core.schemas import GenerateRequest, JobStatus
from backend.core.job_store import get_job, list_jobs, subscribe, unsubscribe
from backend.services.pipeline import submit_job
import mimetypes

mimetypes.add_type('application/javascript', '.js')
mimetypes.add_type('text/css', '.css')
mimetypes.add_type('image/svg+xml', '.svg')


app = FastAPI(title="AutoCourse Studio API", version="0.2.0")
ROOT = project_root()
FRONTEND = ROOT / "frontend_v2" / "dist"

# If the dist folder doesn't exist yet, fallback to original frontend to prevent startup errors
if not FRONTEND.exists():
    FRONTEND = ROOT / "frontend"

app.mount("/static", StaticFiles(directory=str(FRONTEND)), name="static")
assets_dir = FRONTEND / "assets"
if assets_dir.exists():
    app.mount("/assets", StaticFiles(directory=str(assets_dir)), name="assets")


# (catch_all moved to bottom)



@app.get("/api/health")
def health():
    cfg = get_config()
    return {
        "ok": True,
        "project": cfg.get("project_name", "AutoCourse Studio"),
        "planner_model": cfg.get("providers", {}).get("planner_model", "qwen3:14b"),
        "coding_model": cfg.get("providers", {}).get("coding_model", "qwen2.5:7b"),
        "utility_model": cfg.get("providers", {}).get("utility_model", "gemma3:4b"),
        "ollama_url": cfg.get("providers", {}).get("ollama_url", "http://127.0.0.1:11434"),
    }


@app.get("/api/modes")
def modes():
    return {
        "modes": [
            {"id": "manual_course", "name": "Manual Course Mode", "visuals": "Manim Course / Local Clips", "batch": True},
            {"id": "story", "name": "Story Mode", "visuals": "ComfyUI Story", "batch": False},
            {"id": "youtube_extract", "name": "YouTube Extraction Mode", "visuals": "Auto selected", "batch": False},
            {"id": "autonomous", "name": "Autonomous Mode", "visuals": "Auto selected", "batch": True},
        ],
        "visual_styles": ["manim_course", "comfyui_story", "pexels", "hybrid"],
    }


@app.post("/api/jobs")
def create(req: GenerateRequest):
    try:
        return submit_job(req)
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})


@app.get("/api/jobs")
def jobs():
    return list_jobs()


@app.get("/api/jobs/{job_id}")
def job(job_id: str):
    rec = get_job(job_id)
    if not rec:
        raise HTTPException(404, "Job not found")
    return rec


@app.post("/api/jobs/{job_id}/cancel")
def cancel_job(job_id: str):
    rec = get_job(job_id)
    if not rec:
        raise HTTPException(404, "Job not found")
    if rec.status in [JobStatus.completed, JobStatus.failed, JobStatus.cancelled]:
        return {"message": "Job already finished or cancelled"}
    
    from backend.core.job_store import update_job
    update_job(job_id, status=JobStatus.cancelled, message="Cancelled by Admin", current_task="Cancelled", current_model="")
    return {"message": "Job cancelled"}


@app.get("/api/jobs/{job_id}/stream")
async def stream_job(job_id: str):
    rec = get_job(job_id)
    if not rec:
        raise HTTPException(404, "Job not found")
        
    async def event_generator():
        q = subscribe(job_id)
        try:
            yield f"data: {get_job(job_id).model_dump_json()}\n\n"
            while True:
                job = await q.get()
                yield f"data: {job.model_dump_json()}\n\n"
                if job.status in [JobStatus.completed, JobStatus.failed]:
                    break
        finally:
            unsubscribe(job_id, q)
            
    return StreamingResponse(event_generator(), media_type="text/event-stream")

@app.get("/api/admin/plugins")
def get_plugins():
    from backend.services.brain_manager import BrainManager
    return BrainManager.get_plugin_health()

@app.get("/api/config")
def get_configuration():
    return get_config()

@app.post("/api/config")
def update_configuration(new_cfg: dict = Body(...)):
    save_config(new_cfg)
    return {"status": "success", "message": "Configuration updated"}

@app.get("/api/admin/plugins")
def get_plugins():
    from backend.engine_registry import PLUGINS
    res = []
    for p_id, p_class in PLUGINS.items():
        try:
            inst = p_class()
            res.append({
                "plugin": p_id,
                "model": inst.model_name if hasattr(inst, "model_name") else getattr(inst, "MODEL_NAME", "Unknown"),
                "healthy": True,
                "task_types": [t.value for t in inst.supports] if hasattr(inst, "supports") else []
            })
        except Exception as e:
            res.append({
                "plugin": p_id,
                "model": "Unknown",
                "healthy": False,
                "task_types": []
            })
    return res

@app.get("/api/admin/metrics")
def get_metrics():
    import psutil
    cpu = psutil.cpu_percent()
    mem = psutil.virtual_memory()
    jobs_dict = list_jobs()
    jobs_arr = list(jobs_dict.values())
    active_statuses = {JobStatus.planning, JobStatus.rendering, JobStatus.assembling}
    active_jobs = [j for j in jobs_arr if j.get("status") in [s.value for s in active_statuses]]
    queued_jobs = [j for j in jobs_arr if j.get("status") == JobStatus.queued.value]
    
    return {
        "cpu_percent": cpu,
        "ram_percent": mem.percent,
        "ram_used_gb": round(mem.used / (1024**3), 1),
        "ram_total_gb": round(mem.total / (1024**3), 1),
        "active_workers": len(active_jobs),
        "queued_jobs": len(queued_jobs)
    }

@app.get("/api/admin/cache")
def get_cache():
    from backend.services.cache_manager import CacheManager
    return CacheManager.get_cache_stats()

@app.get("/api/download")
def download(path: str = Query(..., description="Absolute path to a generated file")):
    """Download a generated file by absolute path. Only files inside the outputs directory are allowed."""
    try:
        file_path = Path(path).resolve()
    except Exception:
        raise HTTPException(400, "Invalid path")

    outputs_dir = (ROOT / "outputs").resolve()
    
    # Windows-safe comparison: normalize both paths to lowercase for comparison
    file_str = str(file_path).replace("\\", "/").lower()
    outputs_str = str(outputs_dir).replace("\\", "/").lower()
    
    if not file_str.startswith(outputs_str):
        raise HTTPException(403, f"Access denied: file must be inside the outputs directory. Got: {file_path}")

    if not file_path.exists() or not file_path.is_file():
        raise HTTPException(404, f"File not found: {file_path}")

    return FileResponse(
        file_path,
        filename=file_path.name,
        media_type="video/mp4" if file_path.suffix == ".mp4" else None,
        headers={"Content-Disposition": f'attachment; filename="{file_path.name}"'}
    )

@app.get('/{full_path:path}')
def catch_all(full_path: str):
    if full_path.startswith('api/'):
        raise HTTPException(status_code=404, detail='API route not found')
        
    # Check if the requested file exists in the FRONTEND directory
    file_path = FRONTEND / full_path
    if file_path.exists() and file_path.is_file():
        return FileResponse(file_path)
        
    index_file = FRONTEND / 'index.html'
    if index_file.exists():
        return FileResponse(index_file)
    return JSONResponse(status_code=404, content={'error': 'Frontend build not found. Run npm run build in frontend_v2'})

