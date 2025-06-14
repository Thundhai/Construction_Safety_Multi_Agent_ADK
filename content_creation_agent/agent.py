from google.adk import Agent
import random

class ContentCreationAgent(Agent):
    def __init__(self):
        super().__init__(
            name="ContentCreationAgent",
            description="Creates social media and voice-over content for construction safety.",
            instructions="Generate creative content including captions, descriptions, or scripts based on platform."
        )

    def run(self, context: RuntimeContext) -> None:
        task = context.task
        context.logger.info(f"📥 Received task: {task}")

        task_name = task.get("task_name", "").lower()
        data_summary = task.get("data_summary", "")
        language = task.get("language", "en")

        output = ""

        if "instagram" in task_name:
            output = random.choice([
                "🏗️ Safety first on every site! #ConstructionLife",
                "👷‍♂️ PPE isn't optional—it's life-saving! #SiteSafety",
                "🔍 Spot the hazard before it spots you! #BeAware"
            ])
        elif "tiktok" in task_name:
            output = random.choice([
                "🎬 TikTok Safety Reel: Wear your gear, save a life! #JobsiteReady",
                "🚨 One mistake can cost everything. Stay alert. #ConstructionTok",
                "👷‍♀️ AI-powered safety tips coming your way! #SmartSite"
            ])
        elif "voice-over" in task_name:
            output = (
                "Welcome to our construction site safety briefing. "
                "Always wear your helmet, high-visibility vest, and boots. "
                "Report any unsafe behavior. Stay alert, stay safe."
            )
        else:
            output = "⚠️ Task type not recognized by ContentCreationAgent."

        if language != "en":
            output = f"[Translated to {language.upper()}] {output}"

        context.logger.info(f"✅ Content Generated: {output}")
        context.complete({"content": output})

def get_agent():
    return ContentCreationAgent()
