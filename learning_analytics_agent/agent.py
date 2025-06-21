from google.adk import Agent, RuntimeContext

class LearningAnalyticsAgent(Agent):
    def __init__(self):
        super().__init__(
            name="LearningAnalyticsAgent",
            description="Analyzes user interaction data with safety content to provide learning insights and improvement suggestions.",
            model="gemini-2.0-pro"
        )

    async def run(self, context: RuntimeContext) -> None:
        task = context.task
        analytics_data = task.get("analytics_data", {})

        if not analytics_data:
            context.logger.warning("No analytics data provided.")
            context.complete({
                "status": "failed",
                "reason": "Missing 'analytics_data' field."
            })
            return

        context.logger.info("📊 Analyzing learning interaction data...")

        prompt = (
            "You are an expert learning analytics analyst.\n"
            "Given the following analytics data from a safety training program, provide:\n"
            "- Summary of user engagement and completion\n"
            "- Weak points in understanding\n"
            "- Recommendations to improve the learning experience\n\n"
            f"Data:\n{analytics_data}"
        )

        result = await context.llm.complete(prompt)

        context.logger.info("✅ Learning analysis complete.")
        context.complete({
            "status": "success",
            "insights": result.text.strip()
        })

def get_agent():
    return LearningAnalyticsAgent()
