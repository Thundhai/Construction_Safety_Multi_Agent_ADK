from google.adk import Agent


class ComplianceCheckerAgent(Agent):
    def __init__(self):
        super().__init__(
            name="ComplianceCheckerAgent",
            description="Checks text for compliance with global safety standards using LLM or rule-based logic.",
            model="gemini-2.0-pro"
        )

    async def run(self, context: RuntimeContext) -> None:
        task = context.task
        input_type = task.get("input_type", "content").lower()
        mode = task.get("mode", "llm").lower()
        text = task.get("text", "").strip()

        if not text:
            context.logger.warning("No text provided for compliance checking.")
            context.complete({
                "compliance_status": "non-compliant",
                "reason": "No text provided.",
                "recommendations": [],
                "violated_standards": []
            })
            return

        context.logger.info(f"🔍 Checking {input_type} text in {mode.upper()} mode...")

        if mode == "rule_based":
            result = self.rule_based_check(text)
            context.complete(result)
            return

        # Default: LLM mode
        prompt = (
            f"You are a global safety compliance auditor. "
            f"Check the following {input_type} against global safety standards including:\n"
            f"- OSHA (USA)\n"
            f"- ISO 45001\n"
            f"- HSE (UK)\n"
            f"- GB/T standards (China)\n\n"
            f"Text:\n{text}\n\n"
            f"Instructions:\n"
            f"1. Determine if it’s compliant.\n"
            f"2. List violated standards, if any.\n"
            f"3. Provide recommendations.\n\n"
            f"Respond in JSON with fields: compliance_status, recommendations, violated_standards."
        )

        response = await context.llm.complete(prompt)

        try:
            parsed = context.safe_json_loads(response)
            context.complete(parsed)
        except Exception as e:
            context.logger.error(f"❌ Failed to parse LLM response: {e}")
            context.complete({
                "compliance_status": "non-compliant",
                "reason": "Unable to parse LLM response.",
                "recommendations": ["Use standard safety language.", "Clarify unclear risk areas."],
                "violated_standards": []
            })

    def rule_based_check(self, text: str) -> dict:
        """
        Simple keyword check to simulate compliance validation.
        """
        keywords_required = ["PPE", "hazard", "risk assessment", "training", "emergency"]
        violations = [kw for kw in keywords_required if kw.lower() not in text.lower()]

        if violations:
            return {
                "compliance_status": "non-compliant",
                "reason": "Missing key safety terms.",
                "recommendations": [f"Include mention of '{kw}'." for kw in violations],
                "violated_standards": ["General Safety Guidelines"]
            }
        return {
            "compliance_status": "compliant",
            "reason": "All critical safety keywords present.",
            "recommendations": [],
            "violated_standards": []
        }


def get_agent():
    return ComplianceCheckerAgent()

