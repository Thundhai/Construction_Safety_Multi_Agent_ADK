from google.adk import Agent


class VoiceOverAgent(Agent):
    def __init__(self):
        super().__init__(
            name="VoiceOverAgent",
            description="Generates voice-over scripts for construction safety content.",
            model="gemini-2.0-pro"
        )

    async def run(self, context: RuntimeContext) -> None:
        task = context.task
        content = task.get("content", "")

        if not content:
            context.logger.warning("No content provided for voice-over.")
            context.complete({
                "status": "failed",
                "reason": "No content provided."
            })
            return

        context.logger.info("🎤 Generating voice-over script...")

        prompt = (
            "You are a professional voice-over scriptwriter. "
            "Rewrite the following content for an engaging voice narration script. "
            "Ensure it sounds conversational and clear, suitable for a 30–60 second audio clip.\n\n"
            f"Content:\n{content}"
        )

        result = await context.llm.complete(prompt)

        context.logger.info("✅ Voice-over script generated.")
        context.complete({
            "status": "success",
            "voice_over_script": result.strip()
        })

def get_agent():
    return VoiceOverAgent()
