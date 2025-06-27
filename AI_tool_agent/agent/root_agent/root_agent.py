# tech_ai_team_adk/agent/root_agent.py

from google.adk import Agent

class RootAgent(Agent):
    def __init__(self):
        super().__init__(
            name="RootAgent",
            description="Coordinates sub-agents for safety content creation and analysis.",
            model="gemini-2.0-flash"
        )

    async def run(self, context) -> None:
        task_input = context.input.strip().lower()
        context.logger.info(f"📥 Received task: {task_input}")

        result = {}

        if "caption" in task_input or "tiktok" in task_input:
            context.logger.info("📝 Routing to Content Creation Agent")
            response = await context.call("content_creation_agent", input=task_input)
            result["content_creation"] = response.output

        elif "translate" in task_input:
            context.logger.info("🌍 Routing to Translator Agent")
            response = await context.call("translator_agent", input=task_input)
            result["translation"] = response.output

        elif "voice" in task_input or "script" in task_input:
            context.logger.info("🎤 Routing to Voiceover Agent")
            response = await context.call("voiceover_agent", input=task_input)
            result["voiceover"] = response.output

        elif "risk" in task_input or "hazard" in task_input:
            context.logger.info("⚠️ Routing to Risk Assessment Agent")
            response = await context.call("risk_assessment_agent", input=task_input)
            result["risk_assessment"] = response.output

        elif "audience" in task_input:
            context.logger.info("👥 Routing to Audience Analysis Agent")
            response = await context.call("audience_analysis_agent", input=task_input)
            result["audience_analysis"] = response.output

        elif "localize" in task_input or "adapt" in task_input:
            context.logger.info("🌐 Routing to Content Localization Agent")
            response = await context.call("content_localization_agent", input=task_input)
            result["localization"] = response.output

        elif "usability" in task_input:
            context.logger.info("🧪 Routing to Usability Testing Agent")
            response = await context.call("usability_testing_agent", input=task_input)
            result["usability_testing"] = response.output

        elif "analytics" in task_input or "interaction" in task_input:
            context.logger.info("📊 Routing to Learning Analytics Agent")
            response = await context.call("learning_analytics_agent", input=task_input)
            result["analytics"] = response.output
        elif "style" in task_input or "tone" in task_input:
            context.logger.info("🎨 Routing to Style & Tone Agent")
            response = await context.call("style_tone_agent", input=task_input)
            result["style_tone"] = response.output

        else:
            context.logger.warning("🤷 Unknown request — no suitable agent found.")
            result["error"] = "No matching sub-agent for input."

        context.complete(result)

def get_agent():
    return RootAgent()


root_agent = RootAgent()
