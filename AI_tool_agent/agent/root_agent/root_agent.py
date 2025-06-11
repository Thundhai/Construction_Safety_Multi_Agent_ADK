from google.adk import Agent

class RootAgent(Agent):
    def run(self, context: object) -> None:
        context.logger.info("✅ RootAgent is running!")
        print("🎉 Tech_AI_Team agent initialized successfully.")

def get_agent() -> Agent:
    return RootAgent(
        name="TechAITeam",
        description="The master coordinator for the tech AI team project.",
        model="chat-bison"
    )

