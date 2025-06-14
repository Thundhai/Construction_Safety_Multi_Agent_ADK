from google.adk import Agent


class RootAgent(Agent):
    def __init__(self):
        super().__init__(
            name="RootAgent",
            description="Orchestrates subtasks for safety content, compliance, and voice-over narration.",
            model="gemini-2.0-flash"
        )

    async def run(self, context) -> None:
        task = context.task
        context.logger.info(f"📥 RootAgent received task: {task}")

        user_prompt = task.get("input", "")
        context.logger.info(f"🔍 User prompt: {user_prompt}")

        # Step 1: Decide which DataEngineerAgent subtasks to run
        subtasks = []
        lowered = user_prompt.lower()
        if "collect" in lowered:
            subtasks.append("Collect Site Data")
        if "clean" in lowered:
            subtasks.append("Clean Site Data")
        if "preprocess" in lowered:
            subtasks.append("Preprocess Site Data")
        if "process" in lowered or not subtasks:
            subtasks.append("Process Site Data")

        # Step 2: Run DataEngineerAgent tasks
        data_outputs = []
        for task_name in subtasks:
            context.logger.info(f"📤 Sending '{task_name}' to DataEngineerAgent...")
            result = await context.run_subtask(
                agent="data_engineer_agent",
                input={"task_name": task_name}
            )
            context.logger.info(f"✅ Result from '{task_name}': {result}")
            data_outputs.append(result.get("result", f"{task_name} done."))

        combined_summary = "\n".join(data_outputs)

        # Step 3: Generate social media content
        context.logger.info("📝 Sending to ContentCreationAgent...")
        content_result = await context.run_subtask(
            agent="content_creation_agent",
            input={
                "task_name": "Generate Instagram Caption",
                "data_summary": combined_summary
            }
        )
        content = content_result.get("content", "No content generated.")
        context.logger.info(f"✅ ContentCreationAgent result: {content}")

        # Step 4: Check compliance
        context.logger.info("📋 Sending to ComplianceCheckerAgent...")
        compliance_result = await context.run_subtask(
            agent="compliance_checker_agent",
            input={
                "input_type": "content",
                "text": content
            }
        )
        context.logger.info(f"✅ Compliance result: {compliance_result}")

        # Step 5: Generate voice-over narration
        context.logger.info("🎙️ Sending to VoiceOverAgent...")
        voice_result = await context.run_subtask(
            agent="voice_over_agent",
            input={
                "text": content,
                "audience": "construction safety workers"
            }
        )
        narration_script = voice_result.get("narration_script", "No narration generated.")
        context.logger.info(f"✅ VoiceOverAgent result: {narration_script}")

        # Final output
        context.complete({
            "summary": "AI pipeline completed based on user prompt.",
            "data_summary": combined_summary,
            "content": content,
            "compliance": compliance_result,
            "narration_script": narration_script
        })


def get_agent():
    return RootAgent()

