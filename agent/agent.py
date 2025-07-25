from google.adk import Agent
from typing import Optional, Dict, Any

class RootAgent(Agent):
    def __init__(self):
        super().__init__(
            name="RootAgent",
            description="Advanced orchestrator with memory, reasoning, and safety features.",
            model="gemini-2.0-flash"
        )

    async def run(self, context) -> None:
        task_input = context.input

        # Extract input and metadata
        if isinstance(task_input, dict):
            task_text = task_input.get("input", "").strip().lower()
            meta = task_input.get("meta", {})
        else:
            task_text = str(task_input).strip().lower()
            meta = {}

        dry_run = meta.get("dry_run", False)
        context.logger.info(f"📥 Received task: {task_text}")

        # Memory mock fallback
        if hasattr(context, "memory"):
            context.memory["last_task"] = task_text
            context.memory["last_meta"] = meta

        # Decide routing
        route, reason = self.decide_route(task_text, meta)
        context.logger.info(f"📡 Routing to: {route} | Reason: {reason}")

        if dry_run:
            context.complete({"route": route, "reason": reason, "dry_run": True})
            return

        if not route:
            context.complete({"status": "failed", "reason": "No matching agent found."})
            return

        # Call sub-agent
        try:
            response = await context.call(route, input=task_text)
            output = response.output

            # Optional: Safety checks
            if isinstance(output, str) and len(output) < 20:
                context.logger.warning("⚠️ Output may be too short. Review required.")
            if "compliance" in task_text:
                context.logger.warning("⚠️ Possible legal compliance issue. Review suggested.")

            context.complete({
                "agent": route,
                "output": output,
                "reason": reason
            })
        except Exception as e:
            context.logger.error(f"❌ Error routing to agent: {e}")
            context.complete({"error": str(e), "agent": route})

    def decide_route(self, task: str, meta: Optional[Dict[str, Any]] = None) -> (Optional[str], str):
        task = task.lower()
        meta = meta or {}

        if any(k in task for k in ["risk", "hazard", "exposure"]):
            return "risk_assessment_agent", "Matched risk"
        elif any(k in task for k in ["inspection", "image", "violation", "drone", "photo"]):
            return "inspection_audit_agent", "Matched inspection"
        elif any(k in task for k in ["training", "certification", "license", "gap"]):
            return "training_compliance_agent", "Matched training"
        elif any(k in task for k in ["incident", "accident", "near miss", "root cause"]):
            return "incident_management_agent", "Matched incident"
        elif any(k in task for k in ["environment", "pollution", "sensor", "gas", "noise"]):
            return "environmental_monitoring_agent", "Matched environment"
        elif any(k in task for k in ["translate", "yoruba", "hausa", "swahili", "french"]):
            return "translation_agent", "Matched translation"
        elif "audience" in task:
            return "audience_analysis_agent", "Matched audience"
        elif "compliance" in task or "standard" in task:
            return "compliance_checker_agent", "Matched compliance"
        elif "analytics" in task or "completion rate" in task:
            return "learning_analytics_agent", "Matched analytics"
        elif any(k in task for k in ["data clean", "normalize", "raw data"]):
            return "data_engineer_agent", "Matched data prep"
        elif any(k in task for k in ["reflect", "why", "bias", "feedback"]):
            return "reflective_agent", "Matched reflection"

        return "reflective_agent", "Default fallback"


def get_agent():
    return RootAgent()

# ADK expects a variable named 'root_agent' for discovery
root_agent = RootAgent()
