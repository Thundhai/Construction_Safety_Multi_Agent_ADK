from google.adk import Agent, RuntimeContext

class ContentLocalizationAgent(Agent):
    def __init__(self):
        super().__init__(
            name="ContentLocalizationAgent",
            description="Adapts safety content to fit cultural norms, values, and communication styles of the target audience.",
            model="gemini-2.0-pro"
        )

    async def run(self, context: RuntimeContext) -> None:
        task = context.task
        content = task.get("content", "")
        target_culture = task.get("target_culture", "")

        if not content or not target_culture:
            context.logger.warning("Missing content or target_culture.")
            context.complete({
                "status": "failed",
                "reason": "Missing 'content' or 'target_culture'."
            })
            return

        context.logger.info(f"🌍 Localizing content for culture: {target_culture}")

        prompt = (
            "You are a cultural communication specialist tasked with adapting safety messages.\n\n"
            f"Content: {content}\n\n"
            f"Target Culture: {target_culture}\n\n"
            "Rewrite the content to be culturally appropriate, respectful, and clearly understood by the target audience. "
            "Adjust idioms, tone, examples, and communication style if needed. Do NOT simply translate — localize contextually.\n\n"
            "Return only the adapted version."
        )

        result = await context.llm.complete(prompt)

        context.logger.info("✅ Content localized.")
        context.complete({
            "status": "success",
            "target_culture": target_culture,
            "localized_content": result.text.strip()
        })


def get_agent():
    return ContentLocalizationAgent()
