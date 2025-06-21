from google.adk import Agent

class ComplianceCheckerAgent(Agent):
    def __init__(self):
        super().__init__(
            name="ComplianceCheckerAgent",
            description="Checks text for compliance with global safety standards using LLM or rule-based logic.",
            model="gemini-2.0-pro"
        )

    async def run(self, context) -> None:
        content = context.input
        if not content:
            context.logger.warning("[ComplianceCheckerAgent] No text provided for compliance checking.")
            context.complete({
                "compliance": "non-compliant",
                "reason": "No text provided.",
                "recommendations": [],
                "violated_standards": []
            })
            return
        context.logger.info("[ComplianceCheckerAgent] Checking content for compliance.")
        if hasattr(context.llm, 'complete'):
            # Example: call LLM for compliance (stubbed for now)
            compliance = "Compliant" if "OSHA" in content else "Needs review"
        else:
            compliance = "[Stub] Compliance check for: " + content
        context.complete({
            "compliance_status": compliance,
            "recommendations": ["Include OSHA standards."],
            "violated_standards": [] if compliance == "Compliant" else ["OSHA"]
        })


def get_agent():
    return ComplianceCheckerAgent()

