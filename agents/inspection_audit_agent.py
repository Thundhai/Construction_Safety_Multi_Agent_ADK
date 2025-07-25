from adk_local import RuntimeContext
from adk_local import Agent  # optionally alias Agent if needed

from ultralytics import YOLO
from PIL import Image
import base64
import io
import os

# Optional reporting tool (make sure this module exists)
try:
    from utils.reporting import generate_inspection_report
except ImportError:
    generate_inspection_report = None  # If not available, skip PDF generation

os.makedirs("reports", exist_ok=True)

class InspectionAuditAgent(Agent):
    def __init__(self):
        super().__init__(
            name="InspectionAuditAgent",
            description="Uses computer vision to detect safety violations in construction site images.",
            model="gemini-2.0-pro"
        )
        self.model = YOLO("yolov5s.pt")  # Ensure yolov5s.pt is available locally or download automatically

    async def run(self, context: RuntimeContext) -> None:
        task = context.task
        image_b64 = task.get("image_base64", "")

        if not image_b64:
            context.complete({"status": "failed", "reason": "No image provided"})
            return

        try:
            image_bytes = base64.b64decode(image_b64)
            image = Image.open(io.BytesIO(image_bytes))

            results = self.model(image)
            labels = results[0].names
            detailed_violations = []
            summary_violations = []
            for box in results[0].boxes:
                cls_id = int(box.cls)
                confidence = float(box.conf)
                label = labels[cls_id]
                xyxy = box.xyxy[0].tolist() if hasattr(box, 'xyxy') else None
                detailed_violations.append({
                    "label": label,
                    "confidence": confidence,
                    "bbox": xyxy,
                    "recommendation": self.recommend_action(label)
                })
                summary_violations.append(label)

            if generate_inspection_report:
                generate_inspection_report([v["label"] for v in detailed_violations], "reports/inspection_report.pdf")

            # Call Compliance, Risk, and Incident agents with a summary of violations
            summary_text = ", ".join(summary_violations) if summary_violations else "No violations detected."
            compliance_result = await context.call("ComplianceCheckerAgent", {"input": summary_text})
            risk_result = await context.call("RiskAssessmentAgent", {"input": summary_text})
            incident_result = await context.call("IncidentManagementAgent", {"incident_description": summary_text})

            context.logger.info("✅ Vision analysis complete.")
            context.complete({
                "status": "success",
                "detailed_violations": detailed_violations,
                "summary_violations": summary_violations,
                "compliance_analysis": compliance_result,
                "risk_assessment": risk_result,
                "incident_analysis": incident_result,
                "rules_summary": self.rules_summary()
            })

        except Exception as e:
            context.logger.error(f"Error in image processing: {e}")
            context.complete({
                "status": "error",
                "message": str(e)
            })

    @staticmethod
    def recommend_action(label):
        # Map label to recommended action
        actions = {
            "person": "Ensure all personnel wear PPE.",
            "helmet": "Ensure helmet is worn correctly.",
            "gloves": "Wear protective gloves.",
            "vest": "Wear high-visibility vest.",
            "ladder": "Ensure ladder is stable and used safely.",
            "scaffold": "Inspect scaffold for safety compliance.",
            "harness": "Use fall protection harness.",
            "electrical": "Check for exposed wiring and lockout/tagout.",
            # Add more mappings as needed
        }
        return actions.get(label.lower(), f"Review safety compliance for {label}.")

    @staticmethod
    def rules_summary():
        return [
            "Detects safety violations in images using YOLO.",
            "Outputs bounding box, label, confidence, and recommended action for each detection.",
            "Calls ComplianceCheckerAgent, RiskAssessmentAgent, and IncidentManagementAgent with detected violations.",
            "Aggregates and reports all results for explainability."
        ]

# ADK CLI support
async def run_with_adk(task: dict) -> dict:
    agent = InspectionAuditAgent()
    return await agent.run_with_adk(task)

def get_agent():
    return InspectionAuditAgent()
