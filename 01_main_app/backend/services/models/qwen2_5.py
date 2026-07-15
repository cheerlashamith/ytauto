from backend.services.models.base_plugin import AIModelPlugin
from backend.core.schemas import TaskType

class Qwen25Plugin(AIModelPlugin):
    def model_name(self) -> str:
        return "qwen2.5:7b"
        
    def supports_task(self, task: TaskType) -> bool:
        return task in [TaskType.CODE, TaskType.PLANNING, TaskType.STORY, TaskType.SYLLABUS]
