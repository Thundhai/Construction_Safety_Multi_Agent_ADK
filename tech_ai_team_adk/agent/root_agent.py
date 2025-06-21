from google.adk import Agent

class RootAgent(Agent):
    def __init__(self):
        super().__init__(name="RootAgent")

    async def run(self, context):
        task_input = context.input.strip().lower()
        result = {}

        if "caption" in task_input or "tiktok" in task_input:
            response = await context.call("ContentCreationAgent", input=task_input)
            result["content_creation"] = response.output
        elif "translate" in task_input:
            response = await context.call("TranslationAgent", input=task_input)
            result["translation"] = response.output
        elif "voice" in task_input or "script" in task_input:
            response = await context.call("VoiceOverAgent", input=task_input)
            result["voiceover"] = response.output
        elif "risk" in task_input or "hazard" in task_input:
            response = await context.call("RiskAssessmentAgent", input=task_input)
            result["risk_assessment"] = response.output
        elif "audience" in task_input:
            response = await context.call("AudienceAnalysisAgent", input=task_input)
            result["audience_analysis"] = response.output
        elif "localize" in task_input or "adapt" in task_input:
            response = await context.call("ContentLocalizationAgent", input=task_input)
            result["localization"] = response.output
        elif "usability" in task_input:
            response = await context.call("UsabilityTestingAgent", input=task_input)
            result["usability_testing"] = response.output
        elif "analytics" in task_input or "interaction" in task_input:
            response = await context.call("LearningAnalyticsAgent", input=task_input)
            result["analytics"] = response.output
        elif "style" in task_input or "tone" in task_input:
            response = await context.call("StyleToneAnalysisAgent", input=task_input)
            result["style_tone"] = response.output
        else:
            result["error"] = "No matching sub-agent for input."

        context.complete(result)
