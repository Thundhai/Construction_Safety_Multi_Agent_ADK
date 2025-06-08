# TaskAgent main class 

from typing import Any, Dict
from adk.agent.agent import BaseAgent
from adk.types import Message

class TaskAgent(BaseAgent):
    def __init__(self, agent_config: Dict[str, Any]):
        super().__init__(agent_config)

    def register_methods(self):
        self.register_method("handle_task", self.handle_task)

    def handle_task(self, message: Message) -> str:
        task_details = message.payload.get("task", "No task specified.")
        print(f"[TaskAgent] Received task: {task_details}")
        return f"Task received: {task_details}"

