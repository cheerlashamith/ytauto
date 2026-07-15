from backend.services.models.base_plugin import AIModelPlugin
from backend.core.schemas import TaskType

class Gemma3Plugin(AIModelPlugin):
    def model_name(self) -> str:
        return "gemma3:4b"
        
    def supports_task(self, task: TaskType) -> bool:
        return task in [TaskType.KEYWORDS, TaskType.CLASSIFY, TaskType.ENRICHMENT, TaskType.PLANNING, TaskType.STORY, TaskType.SYLLABUS]
