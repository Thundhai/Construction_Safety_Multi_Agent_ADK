from google.adk import Agent

class TranslationAgent(Agent):
    def __init__(self):
        super().__init__(name="TranslationAgent")

    async def run(self, context):
        content = context.input
        context.logger.info("[TranslationAgent] Translating content.")
        if hasattr(context.llm, 'complete'):
            # Example: call LLM for each language (stubbed for now)
            translations = {
                "French": f"[French] {content}",
                "Spanish": f"[Spanish] {content}"
            }
        else:
            translations = {
                "French": f"[Stub] French translation for: {content}",
                "Spanish": f"[Stub] Spanish translation for: {content}"
            }
        context.complete({"translations": translations})

def get_agent():
    return TranslationAgent()
