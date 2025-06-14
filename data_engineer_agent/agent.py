from google.adk import Agent
from google.cloud.agent_app.runtime_context import RuntimeContext
import time
import random

class DataEngineerAgent(Agent):
    def __init__(self):
        super().__init__(
            name="DataEngineerAgent",
            description="Processes raw construction safety data to prepare it for analysis.",
            instructions="Collect, clean, process, and preprocess site data to prepare for insights."
        )

    def run(self, context: RuntimeContext) -> None:
        task = context.task
        context.logger.info(f"📥 Received task: {task}")

        task_name = task.get("task_name", "")
        output = ""

        if "Collect" in task_name:
            output = self.collect_data()
        elif "Clean" in task_name:
            output = self.clean_data()
        elif "Process" in task_name:
            output = self.process_data()
        elif "Preprocess" in task_name:
            output = self.preprocess_data()
        else:
            output = f"⚠️ Unknown task: {task_name}"
            context.logger.warn(output)
            context.complete({"error": output})
            return

        context.logger.info(f"✅ Completed: {task_name}")
        context.complete({"result": output})

    def collect_data(self):
        time.sleep(1)
        return "📦 Raw data collected from construction logs."

    def clean_data(self):
        time.sleep(1)
        return "🧼 Data cleaned and null values removed."

    def process_data(self):
        time.sleep(1)
        return "🛠️ Data processed and structured."

    def preprocess_data(self):
        time.sleep(1)
        return "⚙️ Data normalized and ready for analysis."

def get_agent():
    return DataEngineerAgent()
