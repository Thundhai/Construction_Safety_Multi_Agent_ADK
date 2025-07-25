from adk_local import RuntimeContext
from adk_local import Agent  # optionally alias Agent if needed

import spacy
from datetime import datetime

class IncidentManagementAgent(Agent):
    def __init__(self):
        super().__init__(
            name="IncidentManagementAgent",
            description="Analyzes incident reports using NLP and suggests actions. Outputs Fishbone format and training.",
            model="gemini-2.0-pro"
        )
        self.nlp = spacy.load("en_core_web_sm")

        # Training mappings by root cause category
        self.training_map = {
            "Slip/Trip/Fall hazard": ["Fall prevention basics", "Scaffold usage training"],
            "Electrical safety failure": ["Electrical hazard awareness", "LOTO procedures"],
            "Equipment safety lapse": ["Machine safety protocols", "Guarding awareness"],
            "Procedural failure": ["Site SOP refresher", "Task-specific procedure training"],
            "Human error": ["Situational awareness", "Fatigue management"],
            "Unclassified": ["General safety re-orientation"]
        }

    async def run(self, context: RuntimeContext) -> None:
        task = context.task
        report_text = task.get("incident_description", "")
        location = task.get("location", "unknown site")
        reporter = task.get("reporter", "anonymous")
        date = task.get("date", None)
        time_of_incident = task.get("time", None)
        people_involved = task.get("people_involved", None)
        immediate_action = task.get("immediate_action", None)

        # Advanced field completeness and rule checks
        missing_fields = []
        recommendations = []
        field_breakdown = {}
        for field, value in [
            ("incident_description", report_text),
            ("location", location),
            ("reporter", reporter),
            ("date", date),
            ("time", time_of_incident),
            ("people_involved", people_involved),
            ("immediate_action", immediate_action)
        ]:
            if not value or (isinstance(value, str) and not value.strip()):
                missing_fields.append(field)
                recommendations.append(f"Add {field.replace('_', ' ')} to the report.")
                field_breakdown[field] = {"present": False, "value": None}
            else:
                field_breakdown[field] = {"present": True, "value": value}

        if not report_text or len(report_text.strip()) < 20:
            recommendations.append("Incident description is too short or missing. Provide a detailed account.")

        # Advanced NLP: NER, action verbs, and cause-effect extraction
        doc = self.nlp(report_text)
        keywords = [token.text for token in doc if token.pos_ in ("NOUN", "VERB") and not token.is_stop]
        action_verbs = [token.lemma_ for token in doc if token.pos_ == "VERB" and not token.is_stop]
        entities = [(ent.text, ent.label_) for ent in doc.ents]
        root_cause = self._identify_root_cause(keywords)

        # Cause-effect extraction using dependency parsing
        cause_effects = []
        for sent in doc.sents:
            for token in sent:
                # Look for patterns like 'X because Y', 'X due to Y', 'X caused by Y', etc.
                if token.dep_ in ("advcl", "prep", "mark") and token.text.lower() in ("because", "due", "caused"):
                    cause = sent.text
                    # Try to extract the effect and cause phrases
                    # Simple heuristic: split on the causal word
                    parts = sent.text.lower().split(token.text.lower(), 1)
                    if len(parts) == 2:
                        effect = parts[0].strip(",. ")
                        cause = parts[1].strip(",. ")
                        cause_effects.append({"effect": effect, "cause": cause, "pattern": token.text.lower()})
        # Also look for 'as a result', 'therefore', etc.
        for sent in doc.sents:
            if "as a result" in sent.text.lower() or "therefore" in sent.text.lower():
                cause_effects.append({"sentence": sent.text, "pattern": "result/therefore"})

        # Build Fishbone structure
        fishbone = self._build_fishbone_structure(root_cause)

        # Get LLM-enhanced analysis
        prompt = (
            f"Incident Report:\n\n{report_text}\n\n"
            "Provide the following:\n"
            "- Incident summary\n"
            "- Root cause\n"
            "- Immediate action\n"
            "- Corrective & Preventive actions\n"
            "- Categorize under: Human Error, Environment, Equipment, Procedure"
        )
        llm_response = await context.llm.complete(prompt)

        # Recommend training
        suggested_training = self.training_map.get(root_cause, self.training_map["Unclassified"])

        # Passive/vague language detection
        vague_terms = ["should", "may", "could", "as appropriate", "if possible", "might"]
        vague_found = [vt for vt in vague_terms if vt in report_text.lower()]
        for vt in vague_found:
            recommendations.append(f"Vague language detected: '{vt}'. Use clear, direct statements.")

        # Agent integration: call ComplianceCheckerAgent and RiskAssessmentAgent
        compliance_result = await context.call("ComplianceCheckerAgent", {"input": report_text})
        risk_result = await context.call("RiskAssessmentAgent", {"input": report_text})

        # Output
        output = {
            "status": "success",
            "report_date": datetime.now().strftime("%Y-%m-%d"),
            "location": location,
            "reporter": reporter,
            "field_breakdown": field_breakdown,
            "missing_fields": missing_fields,
            "keywords": keywords,
            "action_verbs": action_verbs,
            "entities": entities,
            "cause_effects": cause_effects,
            "root_cause": root_cause,
            "suggested_training": suggested_training,
            "fishbone_structure": fishbone,
            "llm_analysis": llm_response.text.strip(),
            "recommendations": list(set(recommendations)),
            "vague_language": vague_found,
            "rules_summary": self.rules_summary(),
            "compliance_analysis": compliance_result,
            "risk_assessment": risk_result
        }
        context.complete(output)

    @staticmethod
    def rules_summary():
        return [
            "Checks for missing or incomplete incident fields (description, location, date, time, people, actions).",
            "Flags vague or passive language in the report.",
            "Performs NLP keyword/root cause extraction.",
            "Builds Fishbone (Ishikawa) structure for root cause analysis.",
            "Suggests corrective/preventive actions and training.",
            "Provides LLM-enhanced incident analysis."
        ]

    def _identify_root_cause(self, keywords):
        if "slip" in keywords or "fall" in keywords:
            return "Slip/Trip/Fall hazard"
        if "electrical" in keywords or "shock" in keywords:
            return "Electrical safety failure"
        if "guard" in keywords or "machine" in keywords:
            return "Equipment safety lapse"
        if "procedure" in keywords or "violation" in keywords:
            return "Procedural failure"
        if "fatigue" in keywords or "inattention" in keywords:
            return "Human error"
        return "Unclassified"

    def _build_fishbone_structure(self, root_cause):
        categories = {
            "Environment": [],
            "Equipment": [],
            "People": [],
            "Procedures": [],
            "Materials": [],
            "Management": []
        }

        # Simple logic for demo purposes
        if root_cause == "Slip/Trip/Fall hazard":
            categories["Environment"].append("Wet surfaces")
            categories["Procedures"].append("No harness")
        elif root_cause == "Electrical safety failure":
            categories["Equipment"].append("Exposed wiring")
            categories["Procedures"].append("No lockout/tagout")
        elif root_cause == "Equipment safety lapse":
            categories["Equipment"].append("Missing guards")
            categories["Management"].append("Lack of equipment audit")
        elif root_cause == "Human error":
            categories["People"].append("Fatigue or distraction")
            categories["Management"].append("Inadequate supervision")

        return categories

# Support for ADK CLI
async def run_with_adk(task: dict) -> dict:
    agent = IncidentManagementAgent()
    return await agent.run_with_adk(task)

def get_agent():
    return IncidentManagementAgent()
