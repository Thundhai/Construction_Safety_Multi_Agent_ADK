from google.adk import Agent

class VoiceOverAgent(Agent):
    def __init__(self):
        super().__init__(
            name="VoiceOverAgent",
            description="Generates voice-over scripts for construction safety content.",
            model="gemini-2.0-pro"
        )

    async def run(self, context) -> None:
        task = context.task
        content = task.get("content", "")
        if not content:
            context.logger.warning("[VoiceOverAgent] No content provided for voice-over.")
            context.complete({
                "status": "failed",
                "reason": "No content provided."
            })
            return
        context.logger.info("[VoiceOverAgent] Generating voice-over script...")
        prompt = (
            "You are a professional voice-over scriptwriter. "
            "Rewrite the following content for an engaging voice narration script. "
            "Ensure it sounds conversational and clear, suitable for a 30–60 second audio clip.\n\n"
            f"Content:\n{content}"
        )
        if hasattr(context.llm, 'complete'):
            result = await context.llm.complete(prompt)
            narration_script = result.text if hasattr(result, 'text') else str(result)
        else:
            narration_script = f"[Stub] Voice-over script for: {content}"
        context.logger.info("[VoiceOverAgent] Voice-over script generated.")
        context.complete({
            "status": "success",
            "narration_script": narration_script
        })

def get_agent():
    return VoiceOverAgent()
