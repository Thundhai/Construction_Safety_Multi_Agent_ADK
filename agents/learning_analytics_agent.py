from adk_local import RuntimeContext
from adk_local import Agent  # optionally alias Agent if needed


class LearningAnalyticsAgent(Agent):
    def __init__(self):
        super().__init__(
            name="LearningAnalyticsAgent",
            description="Analyzes user learning interactions and flags improvement opportunities across training-related tasks.",
            model="gemini-2.0-pro"
        )

    async def run(self, context: RuntimeContext) -> None:
        task = context.task or {}
        analytics_data = task.get("analytics_data", {})
        linked_output = task.get("linked_output", "")
        origin_agent = task.get("from_agent", "")

        if not analytics_data and not linked_output:
            context.logger.warning("❗ No analytics or linked output provided.")
            context.complete({
                "status": "failed",
                "reason": "Missing both 'analytics_data' and 'linked_output'."
            })
            return

        context.logger.info("🔎 LearningAnalyticsAgent: Starting analysis...")

        prompt_parts = [
            "You are an expert in safety training analytics.",
            "Based on the provided data or agent output, summarize:",
            "- User engagement and learning gaps",
            "- Problematic modules or content",
            "- Recommendations to improve retention and delivery",
        ]

        if origin_agent:
            prompt_parts.append(f"- The data originated from the agent: `{origin_agent}`")

        if analytics_data:
            prompt_parts.append(f"\n[Analytics Data]\n{analytics_data}")
        if linked_output:
            prompt_parts.append(f"\n[Linked Output from {origin_agent or 'unknown'}]\n{linked_output}")

        prompt = "\n".join(prompt_parts)
        result = await context.llm.complete(prompt)
        summary = result.text.strip()

        context.complete({
            "status": "success",
            "insights": summary,
            "reviewed_agent": origin_agent or None
        })

# Add this for ADK CLI usage
async def run_with_adk(task: dict) -> dict:
    agent = LearningAnalyticsAgent()
    return await agent.run_with_adk(task)

def get_agent():
    return LearningAnalyticsAgent()
