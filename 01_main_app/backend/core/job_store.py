from __future__ import annotations
import json, uuid, threading, asyncio
from pathlib import Path
from typing import Dict, List
from .schemas import JobRecord, JobStatus, GenerateRequest
from .config import outputs_root

_LOCK = threading.Lock()
_JOBS: Dict[str, JobRecord] = {}
_JOB_EVENTS: Dict[str, List[asyncio.Queue]] = {}

def _load_persisted_jobs() -> None:
    """Load all previously persisted jobs from disk on startup."""
    try:
        root = outputs_root()
        for job_dir in root.iterdir():
            job_file = job_dir / "job.json"
            if job_file.exists():
                try:
                    data = json.loads(job_file.read_text(encoding="utf-8"))
                    rec = JobRecord(**data)
                    _JOBS[rec.job_id] = rec
                except Exception:
                    pass  # Skip corrupted job files
    except Exception:
        pass

# Load persisted jobs at import time
_load_persisted_jobs()

def create_job(req: GenerateRequest) -> JobRecord:
    job_id = uuid.uuid4().hex[:12]
    out = outputs_root() / job_id
    out.mkdir(parents=True, exist_ok=True)
    rec = JobRecord(job_id=job_id, status=JobStatus.queued, request=req, output_dir=str(out), message="Queued")
    with _LOCK:
        _JOBS[job_id] = rec
    save_job(rec)
    return rec

def update_job(job_id: str, **kwargs) -> JobRecord:
    with _LOCK:
        rec = _JOBS[job_id]
        data = rec.model_dump()
        data.update(kwargs)
        rec = JobRecord(**data)
        _JOBS[job_id] = rec
    save_job(rec)
    
    # Notify subscribers
    if job_id in _JOB_EVENTS:
        for q in _JOB_EVENTS[job_id]:
            q.put_nowait(rec)
            
    return rec

def get_job(job_id: str) -> JobRecord | None:
    with _LOCK:
        return _JOBS.get(job_id)

def list_jobs() -> dict:
    """Return all jobs as a dict keyed by job_id (newest first ordering maintained by caller)."""
    with _LOCK:
        # Return as dict so frontend Object.values() works correctly
        return {job_id: rec.model_dump() for job_id, rec in _JOBS.items()}

def save_job(rec: JobRecord) -> None:
    Path(rec.output_dir).mkdir(parents=True, exist_ok=True)
    Path(rec.output_dir, "job.json").write_text(rec.model_dump_json(indent=2), encoding="utf-8")

def subscribe(job_id: str) -> asyncio.Queue:
    q = asyncio.Queue()
    if job_id not in _JOB_EVENTS:
        _JOB_EVENTS[job_id] = []
    _JOB_EVENTS[job_id].append(q)
    return q

def unsubscribe(job_id: str, q: asyncio.Queue) -> None:
    if job_id in _JOB_EVENTS and q in _JOB_EVENTS[job_id]:
        _JOB_EVENTS[job_id].remove(q)

