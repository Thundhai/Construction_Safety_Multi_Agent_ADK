from google.adk import Agent, RuntimeContext

class StyleToneAnalysisAgent(Agent):
    def __init__(self):
        super().__init__(
            name="StyleToneAnalysisAgent",
            description="Analyzes safety scripts and narration to ensure alignment with brand style, tone, and voice guidelines.",
            model="gemini-2.0-pro"
        )

    async def run(self, context: RuntimeContext) -> None:
        task = context.task
        content = task.get("content", "")
        guidelines = task.get("guidelines", "")

        if not content:
            context.logger.warning("No content provided for style and tone analysis.")
            context.complete({
                "status": "failed",
                "reason": "Missing 'content' field."
            })
            return

        context.logger.info("🔍 Analyzing content for style and tone alignment...")

        prompt = (
            "You are a brand voice and tone analyst. Your job is to assess whether the following content aligns with the provided style, tone, and voice guidelines.\n"
            "Identify:\n"
            "- Strengths\n"
            "- Inconsistencies\n"
            "- Suggestions for improvement\n\n"
            f"Brand Guidelines:\n{guidelines or 'Use general professional, clear, and engaging tone.'}\n\n"
            f"Content:\n{content}"
        )

        result = await context.llm.complete(prompt)

        context.logger.info("✅ Style and tone analysis completed.")
        context.complete({
            "status": "success",
            "style_tone_feedback": result.text.strip()
        })

def get_agent():
    return StyleToneAnalysisAgent()
