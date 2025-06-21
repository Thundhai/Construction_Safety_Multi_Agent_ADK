from google.adk import Agent, RuntimeContext

class AudienceAnalysisAgent(Agent):
    def __init__(self):
        super().__init__(
            name="AudienceAnalysisAgent",
            description="Conducts in-depth analysis of the target audience to improve safety content effectiveness.",
            model="gemini-2.0-pro"
        )

    async def run(self, context: RuntimeContext) -> None:
        task = context.task
        audience = task.get("target_audience", "")
        topic = task.get("topic", "")

        if not audience or not topic:
            context.logger.warning("[AudienceAnalysisAgent] Missing audience or topic.")
            context.complete({
                "status": "failed",
                "reason": "Missing 'target_audience' or 'topic'."
            })
            return

        context.logger.info(f"[AudienceAnalysisAgent] Analyzing audience '{audience}' for topic '{topic}'")

        prompt = (
            "You are a behavioral safety expert and communication strategist.\n\n"
            f"Analyze the following for the safety topic '{topic}' and audience '{audience}':\n\n"
            "- Audience’s existing safety knowledge and skill level\n"
            "- Common attitudes and behaviors toward safety\n"
            "- Preferred learning methods (e.g., visual, auditory, experiential)\n"
            "- Cultural or language considerations\n"
            "- Emotional tone and complexity recommendations\n"
            "- Ideal content formats (e.g., infographic, video, hands-on training)\n"
            "- Best communication/delivery methods\n\n"
            "Provide clear, structured bullet points with practical recommendations."
        )

        if hasattr(context.llm, 'complete'):
            result = await context.llm.complete(prompt)
            analysis = result.text if hasattr(result, 'text') else str(result)
        else:
            analysis = f"[Stub] Audience analysis for: {audience}, {topic}"

        context.complete({"analysis": analysis})


def get_agent():
    return AudienceAnalysisAgent()
