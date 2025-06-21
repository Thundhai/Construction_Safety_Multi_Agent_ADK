from google.adk import Agent, RuntimeContext

class UsabilityTestingAgent(Agent):
    def __init__(self):
        super().__init__(
            name="UsabilityTestingAgent",
            description="Conducts simulated usability testing to evaluate the clarity, engagement, and effectiveness of safety content.",
            model="gemini-2.0-pro"
        )

    async def run(self, context: RuntimeContext) -> None:
        task = context.task
        content = task.get("content", "")
        audience_profile = task.get("audience_profile", "general construction workers")

        if not content:
            context.logger.warning("No content provided for usability testing.")
            context.complete({
                "status": "failed",
                "reason": "Missing 'content' field."
            })
            return

        context.logger.info("🔍 Conducting usability testing simulation...")

        prompt = (
            f"You are simulating usability testing with {audience_profile}.\n"
            f"Here is the safety content to evaluate:\n\n"
            f"{content}\n\n"
            "Please provide simulated user feedback that covers:\n"
            "- Clarity of the message\n"
            "- Ease of understanding\n"
            - Engagement level (is it interesting or boring?)\n"
            "- Suggestions to make it more user-friendly\n\n"
            "Return a clear summary of the findings and recommendations for improvement."
        )

        result = await context.llm.complete(prompt)

        context.logger.info("✅ Usability test completed.")
        context.complete({
            "status": "success",
            "audience_profile": audience_profile,
            "usability_feedback": result.text.strip()
        })

def get_agent():
    return UsabilityTestingAgent()
