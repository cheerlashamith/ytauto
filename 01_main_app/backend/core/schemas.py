from __future__ import annotations
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field

class Mode(str, Enum):
    manual_course = "manual_course"
    story = "story"
    youtube_extract = "youtube_extract"
    autonomous = "autonomous"

class VisualStyle(str, Enum):
    manim_course = "manim_course"
    comfyui_story = "comfyui_story"
    pexels = "pexels"
    hybrid = "hybrid"

class JobStatus(str, Enum):
    queued = "queued"
    planning = "planning"
    rendering = "rendering"
    assembling = "assembling"
    completed = "completed"
    failed = "failed"
    cancelled = "cancelled"

class TaskType(str, Enum):
    PLANNING = "planning"
    CODE = "code"
    STORY = "story"
    KEYWORDS = "keywords"
    CLASSIFY = "classify"
    SYLLABUS = "syllabus"
    ENRICHMENT = "enrichment"

class GenerateRequest(BaseModel):
    mode: Mode
    topic: str = Field(default="", min_length=0)
    visual_style: VisualStyle = VisualStyle.manim_course
    syllabus_subject: Optional[str] = None
    selected_units: List[str] = []
    youtube_url: Optional[str] = None
    script_override: Optional[str] = None
    keywords_override: Optional[str] = None
    notes: Optional[str] = None
    # Optional rendering preferences
    aspect: Optional[str] = None  # "16:9" or "9:16"
    voice: Optional[str] = None
    subtitle_enabled: Optional[bool] = None
    bgm_volume: Optional[float] = None

class JobRecord(BaseModel):
    job_id: str
    status: JobStatus
    request: GenerateRequest
    output_dir: str
    message: str = ""
    files: Dict[str, Any] = {}
    progress_percentage: int = 0
    current_task: str = ""
    current_model: str = ""
    created_at: str = Field(default_factory=lambda: datetime.utcnow().isoformat())
