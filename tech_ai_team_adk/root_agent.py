# tech_ai_team_adk/agent/root_agent.py
from tech_ai_team_adk import root_agent

class RootAgent:
    def __init__(self):
        # Remove super().__init__ and set attributes directly
        self.name = "RootAgent"
        self.description = "Coordinates sub-agents for safety content creation and analysis."
        self.model = "gemini-2.0-flash"

    async def run(self, context) -> None:
        task_input = context.input.strip().lower()
        context.logger.info(f"📥 Received task: {task_input}")
        result = {}
        if "caption" in task_input or "tiktok" in task_input:
            context.logger.info("📝 Routing to Content Creation Agent")
            response = await context.call("ContentCreationAgent", input_text=task_input)
            result["content_creation"] = response
        elif "translate" in task_input:
            context.logger.info("🌍 Routing to Translator Agent")
            response = await context.call("TranslationAgent", input_text=task_input)
            result["translation"] = response
        elif "voice" in task_input or "script" in task_input:
            context.logger.info("🎤 Routing to Voiceover Agent")
            response = await context.call("VoiceOverAgent", input_text=task_input)
            result["voiceover"] = response
        elif "risk" in task_input or "hazard" in task_input:
            context.logger.info("⚠️ Routing to Risk Assessment Agent")
            response = await context.call("RiskAssessmentAgent", input_text=task_input)
            result["risk_assessment"] = response
        elif "audience" in task_input:
            context.logger.info("👥 Routing to Audience Analysis Agent")
            response = await context.call("AudienceAnalysisAgent", input_text=task_input)
            result["audience_analysis"] = response
        elif "localize" in task_input or "adapt" in task_input:
            context.logger.info("🌐 Routing to Content Localization Agent")
            response = await context.call("LocalizationAgent", input_text=task_input)
            result["localization"] = response
        elif "usability" in task_input:
            context.logger.info("🧪 Routing to Usability Testing Agent")
            # Stub fallback
            result["usability_testing"] = "[Stub] Usability testing complete."
        elif "analytics" in task_input or "interaction" in task_input:
            context.logger.info("📊 Routing to Learning Analytics Agent")
            # Stub fallback
            result["analytics"] = "[Stub] Analytics complete."
        elif "style" in task_input or "tone" in task_input:
            context.logger.info("🎨 Routing to Style & Tone Agent")
            # Stub fallback
            result["style_tone"] = "[Stub] Style & tone analysis complete."
        else:
            context.logger.warning("🤷 Unknown request — no suitable agent found.")
            result["error"] = "No matching sub-agent for input."
        context.complete(result)

def get_agent():
    return RootAgent()


root_agent = RootAgent()
