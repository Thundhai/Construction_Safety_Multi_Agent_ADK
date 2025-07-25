from adk_local import RuntimeContext
from adk_local import Agent  # optionally alias Agent if needed

import pandas as pd
import time
from typing import Any, Dict, Union

class DataEngineerAgent(Agent):
    def __init__(self):
        super().__init__(
            name="DataEngineerAgent",
            description="Cleans, transforms, and structures safety-related data for analysis or ML training.",
            model="gemini-2.0-pro"
        )

    async def run(self, context: RuntimeContext) -> None:
        task = context.task
        context.logger.info(f"[DataEngineerAgent] Task received: {task}")
        step = task.get("step", "").lower()
        raw_data = task.get("data", None)

        if not step:
            context.complete({"error": "Missing 'step'. Choose from: collect, clean, process, preprocess."})
            return

        try:
            if step == "collect":
                result = self.collect_data()
            elif step == "clean":
                result = self.clean_data(raw_data)
            elif step == "preprocess":
                result = self.preprocess_data(raw_data)
            elif step == "process":
                result = self.process_data(raw_data)
            else:
                result = f"❌ Unknown step: {step}"

            context.complete({"status": "success", "step": step, "result": result})
        except Exception as e:
            context.logger.error(f"[DataEngineerAgent] Error: {e}")
            context.complete({"status": "error", "message": str(e)})

    def collect_data(self) -> str:
        time.sleep(1)
        return "📥 Simulated collection of raw safety logs, sensor files, and CSVs."

    def clean_data(self, data: Union[Dict, str]) -> str:
        df = self._load_data(data)
        df.dropna(inplace=True)
        return df.to_json(orient="records")

    def preprocess_data(self, data: Union[Dict, str]) -> str:
        df = self._load_data(data)
        for col in df.select_dtypes(include=["object"]).columns:
            df[col] = df[col].str.lower().str.strip()
        return df.to_json(orient="records")

    def process_data(self, data: Union[Dict, str]) -> str:
        df = self._load_data(data)
        df["risk_score"] = df.get("incident_count", 0) * 2  # Example feature engineering
        return df.to_json(orient="records")

    def _load_data(self, data, columns=None, sheet_name=None, chunk_size=None):
        from utils.advanced_data_loader import load_data
        result = load_data(data, columns=columns, sheet_name=sheet_name, chunk_size=chunk_size)
        if 'error' in result:
            raise ValueError(result['error'])
        return result['data']

# ✅ For ADK CLI execution
async def run_with_adk(task: dict) -> dict:
    agent = DataEngineerAgent()
    return await agent.run_with_adk(task)

def get_agent():
    return DataEngineerAgent()
