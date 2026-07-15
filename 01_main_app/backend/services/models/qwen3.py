from backend.services.models.base_plugin import AIModelPlugin
from backend.core.schemas import TaskType

class Qwen3Plugin(AIModelPlugin):
    def model_name(self) -> str:
        return "qwen3:14b"
        
    def supports_task(self, task: TaskType) -> bool:
        # qwen3:14b is too large for fast planning — only use for CODE tasks
        # where it's worth the wait. Never use for PLANNING/STORY (causes timeouts).
        return task in [TaskType.CODE]

