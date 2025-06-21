from google.adk import Agent, RuntimeContext

class RiskAssessmentAgent(Agent):
    def __init__(self):
        super().__init__(
            name="RiskAssessmentAgent",
            description="Analyzes a safety topic to identify potential risks, hazards, and vulnerabilities before content creation.",
            model="gemini-2.0-pro"
        )

    async def run(self, context: RuntimeContext) -> None:
        task = context.task
        safety_topic = task.get("topic", "")

        if not safety_topic:
            context.logger.warning("No safety topic provided for risk assessment.")
            context.complete({
                "status": "failed",
                "reason": "No topic provided."
            })
            return

        context.logger.info(f"🔍 Performing risk assessment for topic: {safety_topic}")

        prompt = (
            "You're a safety and risk management expert for construction sites. "
            "Given the following topic, identify:\n"
            "- Key safety hazards\n"
            "- Environmental and human factors\n"
            "- Potential risks and consequences\n"
            "- Recommended safety controls and mitigations\n\n"
            f"Topic: {safety_topic}\n\n"
            "Provide your analysis in a structured bullet-point format."
        )

        result = await context.llm.complete(prompt)

        context.logger.info("✅ Risk assessment completed.")
        context.complete({
            "status": "success",
            "topic": safety_topic,
            "risk_assessment": result.text.strip()
        })


def get_agent():
    return RiskAssessmentAgent()
