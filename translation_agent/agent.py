from google.adk import Agent

class TranslationAgent(Agent):
    def __init__(self):
        super().__init__(
            name="TranslationAgent",
            description="Translates content into requested languages.",
            model="gemini-2.0-flash"
        )

    async def run(self, context: RuntimeContext) -> None:
        task = context.task
        content = task.get("content", "")
        languages = task.get("languages", ["Spanish"])

        translations = {}
        for lang in languages:
            prompt = f"Translate the following content to {lang}:\n\n{content}"
            response = await context.llm.complete(prompt)
            translations[lang] = response.text.strip()

        context.complete({
            "translations": translations
        })

def get_agent():
    return TranslationAgent()
