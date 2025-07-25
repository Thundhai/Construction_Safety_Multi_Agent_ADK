from google.adk import Agent


class ReflectiveAgent(Agent):
    def __init__(self):
        super().__init__(
            name="ReflectiveAgent",
            description="Performs meta-analysis of outputs from other agents to ensure completeness, clarity, and logical consistency.",
            model="gemini-2.0-pro"
        )

    async def run(self, context) -> None:
        task = context.task
        # Advanced loader
        from utils.advanced_data_loader import load_data
        if isinstance(task, str):
            result = load_data(task)
            if 'error' in result:
                context.complete({'error': result['error']})
                return
            df = result['data']
            context.logger.info(f"Loaded file for reflection: {task}, shape: {df.shape}")
            context.complete({"file_preview": df.head().to_dict(), "metadata": result.get('metadata'), "tables": result.get('tables')})
            return
        # CSV support
        if isinstance(task, str) and task.endswith('.csv'):
            import os
            import pandas as pd
            file_path = os.path.join('data', task) if not os.path.isabs(task) else task
            if os.path.exists(file_path):
                df = pd.read_csv(file_path)
                context.logger.info(f"Loaded CSV for reflection: {file_path}, shape: {df.shape}")
                context.complete({"csv_preview": df.head().to_dict()})
                return
        original_agent = task.get("source_agent", "")
        original_output = task.get("output", "")

        if not original_agent or not original_output:
            context.logger.warning("Missing source_agent or output to reflect on.")
            context.complete({
                "status": "failed",
                "reason": "Missing source_agent or output field."
            })
            return

        context.logger.info(f"🔎 Reflecting on output from {original_agent}...")

        prompt = (
            f"You are an expert auditor and reflective analyst.\n"
            f"Review the output from the agent named '{original_agent}'. Assess:\n"
            "- Was the output logically structured?\n"
            "- Did it fully address the input task?\n"
            "- Are there any missing assumptions, biases, or risks?\n"
            "- Suggest one improvement or clarification.\n\n"
            f"Output to reflect on:\n{original_output}"
        )

        result = await context.llm.complete(prompt)
        reflection = result.text.strip()

        context.logger.info("🪞 Reflection complete.")
        context.complete({
            "status": "success",
            "reflection": reflection,
            "agent_reviewed": original_agent
        })

# Add this for ADK compatibility
async def run_with_adk(task: dict) -> dict:
    agent = ReflectiveAgent()
    return await agent.run_with_adk(task)

def get_agent():
    return ReflectiveAgent()
