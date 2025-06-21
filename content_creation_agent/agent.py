from google.adk import Agent
import random

class ContentCreationAgent(Agent):
    def __init__(self):
        super().__init__(
            name="ContentCreationAgent",
            description="Generates safety-related content such as captions, scripts, and safety instructions.",
            model="gemini-2.0-pro"  # You can switch to 'gemini-1.5-pro' if needed
        )

    async def run(self, context) -> None:
        prompt = context.input
        prompt_template = f"""
        You are a professional safety content writer. Create engaging content for the following task:

        Task: {prompt}

        Requirements:
        - Clear, simple language
        - Focus on safety best practices
        - Format content for the specified platform (e.g., Instagram, TikTok, safety briefing)
        - Output should be concise and engaging
        - Example: "Stay safe! Always use a box cutter with care. #HandSafety"
        """
        context.logger.info("[ContentCreationAgent] Generating content for input task.")
        # Use LLM if available, else stub
        if hasattr(context.llm, 'complete'):
            result = await context.llm.complete(prompt_template)
            # If LLM returns an object with .text, use it
            if hasattr(result, 'text'):
                content = result.text
            else:
                content = str(result)
        else:
            content = "[Stub] Content generated for: " + prompt
        context.complete({"content": content})

def get_agent():
    return ContentCreationAgent()
