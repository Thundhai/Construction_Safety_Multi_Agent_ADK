import pandas as pd
import asyncio
import types
# Import your agents
from tech_ai_team_adk import root_agent
from compliance_checker_agent.agent import ComplianceCheckerAgent
from content_creation_agent.agent import ContentCreationAgent
from data_engineer_agent.agent import DataEngineerAgent
from translator_agent.agent import TranslationAgent
from voiceover_agent.agent import VoiceOverAgent
# ...import other agents as needed...

# Map agent names to classes or instances
from types import SimpleNamespace

# --- Add stubs for missing agents ---
try:
    from google.adk import Agent
except ImportError:
    class Agent:
        def __init__(self, name=None):
            self.name = name

class RiskAssessmentAgent(Agent):
    def __init__(self):
        super().__init__(name="RiskAssessmentAgent")
    async def run(self, context):
        context.complete("[Stub] Risk assessment complete.")
class AudienceAnalysisAgent(Agent):
    def __init__(self):
        super().__init__(name="AudienceAnalysisAgent")
    async def run(self, context):
        context.complete("[Stub] Audience analysis complete.")
class ContentStrategyAgent(Agent):
    def __init__(self):
        super().__init__(name="ContentStrategyAgent")
    async def run(self, context):
        context.complete("[Stub] Content strategy complete.")
class ScriptWritingAgent(Agent):
    def __init__(self):
        super().__init__(name="ScriptWritingAgent")
    async def run(self, context):
        context.complete("[Stub] Script writing complete.")
class VideoEditingAgent(Agent):
    def __init__(self):
        super().__init__(name="VideoEditingAgent")
    async def run(self, context):
        context.complete("[Stub] Video editing complete.")
class AudioEngineeringAgent(Agent):
    def __init__(self):
        super().__init__(name="AudioEngineeringAgent")
    async def run(self, context):
        context.complete("[Stub] Audio engineering complete.")
class LocalizationAgent(Agent):
    def __init__(self):
        super().__init__(name="LocalizationAgent")
    async def run(self, context):
        context.complete("[Stub] Localization complete.")
class ContentLocalizationAgent(Agent):
    def __init__(self):
        super().__init__(name="ContentLocalizationAgent")
    async def run(self, context):
        context.complete("[Stub] Content localization complete.")
class UsabilityTestingAgent(Agent):
    def __init__(self):
        super().__init__(name="UsabilityTestingAgent")
    async def run(self, context):
        context.complete("[Stub] Usability testing complete.")
class LearningAnalyticsAgent(Agent):
    def __init__(self):
        super().__init__(name="LearningAnalyticsAgent")
    async def run(self, context):
        context.complete("[Stub] Learning analytics complete.")
class StyleToneAnalysisAgent(Agent):
    def __init__(self):
        super().__init__(name="StyleToneAnalysisAgent")
    async def run(self, context):
        context.complete("[Stub] Style & tone analysis complete.")

AGENT_MAP = {
    "RootAgent": root_agent,
    "ComplianceCheckerAgent": ComplianceCheckerAgent(),
    "ContentCreationAgent": ContentCreationAgent(),
    "DataEngineerAgent": DataEngineerAgent(),
    "TranslationAgent": TranslationAgent(),
    "TranslatorAgent": TranslationAgent(),  # Alias for typo in agent name
    "VoiceOverAgent": VoiceOverAgent(),
    # Add stubs for sub-agents
    "RiskAssessmentAgent": RiskAssessmentAgent(),
    "AudienceAnalysisAgent": AudienceAnalysisAgent(),
    "ContentStrategyAgent": ContentStrategyAgent(),
    "ScriptWritingAgent": ScriptWritingAgent(),
    "VideoEditingAgent": VideoEditingAgent(),
    "AudioEngineeringAgent": AudioEngineeringAgent(),
    "LocalizationAgent": LocalizationAgent(),
    "ContentLocalizationAgent": ContentLocalizationAgent(),
    "UsabilityTestingAgent": UsabilityTestingAgent(),
    "LearningAnalyticsAgent": LearningAnalyticsAgent(),
    "StyleToneAnalysisAgent": StyleToneAnalysisAgent(),
    # ...add other agents here as needed...
}

# Read the CSV, skip the second line (the separator), and use '|' as delimiter
# Also skip blank lines and strip whitespace from all values
with open('input_tasks.csv', 'r', encoding='utf-8') as f:
    lines = f.readlines()
# Remove empty lines
lines = [line for line in lines if line.strip()]
# Write cleaned lines to a temp file for pandas
with open('input_tasks_cleaned.csv', 'w', encoding='utf-8') as f:
    f.writelines(lines)

df = pd.read_csv('input_tasks_cleaned.csv', delimiter='|', skiprows=[1])
df.columns = [col.strip() for col in df.columns]

# Improved context mock for local agent calls
class SimpleContext:
    def __init__(self, input_text):
        self.input = input_text
        self.task = {"input": input_text, "content": input_text, "text": input_text, "task_name": input_text}
        self.logger = type("Logger", (), {"info": print, "warning": print, "warn": print, "error": print})()
        self.complete = lambda result: setattr(self, "result", result)
        async def complete_fn(prompt):
            return "LLM output for: " + prompt
        self.llm = SimpleNamespace(complete=complete_fn)
        self.safe_json_loads = lambda s: {}
    # --- Add call method for sub-agent routing ---
    def call(self, agent_name, input_text=None):
        agent = AGENT_MAP.get(agent_name)
        if not agent:
            raise Exception(f"Sub-agent '{agent_name}' not found.")
        sub_context = SimpleContext(input_text or self.input)
        run_method = getattr(agent, 'run', None)
        if run_method:
            if asyncio.iscoroutinefunction(run_method):
                asyncio.run(run_method(sub_context))
            else:
                run_method(sub_context)
            return getattr(sub_context, "result", None)
        else:
            raise Exception(f"Sub-agent '{agent_name}' has no 'run' method.")

results = []

for i, row in df.iterrows():
    input_text = str(row['input']).strip()
    agent_name = str(row['agent']).strip()

    print(f"🛰️ Processing Task #{i+1}:\n{input_text}\n")

    agent = AGENT_MAP.get(agent_name)
    if not agent:
        output_text = f"❌ Error: Agent '{agent_name}' not found."
    else:
        try:
            context = SimpleContext(input_text)
            run_method = getattr(agent, 'run', None)
            if run_method:
                if asyncio.iscoroutinefunction(run_method):
                    asyncio.run(run_method(context))
                else:
                    run_method(context)
                output_text = getattr(context, "result", "No result returned")
            else:
                output_text = f"❌ Error: Agent '{agent_name}' has no 'run' method."
        except Exception as e:
            output_text = f"❌ Error: {str(e)}"

    print(f"✅ Processed Output:\n{output_text}\n")

    results.append({
        "input": input_text,
        "output": output_text
    })

# Save results
output_df = pd.DataFrame(results)
output_df.to_csv("output_responses.csv", index=False, encoding="utf-8")
print("✅ Done! Results saved to 'output_responses.csv'")
