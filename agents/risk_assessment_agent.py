from google.adk import BaseAgent
import pandas as pd
import json
from durable_rules import ruleset, post
from sklearn.ensemble import RandomForestClassifier
import joblib
import os
import time
import asyncio

from utils.logger import logger
from utils.advanced_data_loader import load_data

class RiskAssessmentAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="risk_assessment_agent",
            description="Analyzes safety risks, predicts incidents, and flags compliance issues for construction operations."
        )

        self.model_path = "models/risk_classifier.joblib"
        self.ml_model = None
        try:
            if os.path.exists(self.model_path):
                self.ml_model = joblib.load(self.model_path)
                logger.info(f"Loaded ML model from {self.model_path}")
            else:
                logger.warning(f"ML model file not found at: {self.model_path}")
        except Exception as e:
            logger.error(f"Failed to load ML model: {e}")

    async def run_with_adk(self, inputs, config=None):
        start_time = time.time()
        topic = inputs.get("topic") or inputs.get("input")
        data_input = inputs.get("data", {})
        files = inputs.get("files", [])

        logger.info(f"Starting risk assessment for topic: {topic}")

        # Handle file input
        file_path = None
        if files and isinstance(files, list) and len(files) > 0:
            file_path = files[0]
        elif isinstance(topic, str) and (topic.endswith(('.csv', '.xlsx', '.xls', '.json', '.pdf', '.txt')) or os.path.exists(topic)):
            file_path = topic

        if file_path:
            try:
                result = load_data(file_path)
                elapsed = round(time.time() - start_time, 3)
                if 'error' in result:
                    logger.error(f"File load failed: {result['error']}")
                    return {'status': 'failed', 'error': result['error'], 'elapsed_sec': elapsed}
                df = result['data']
                logger.info(f"Loaded file: {file_path}, shape: {df.shape}")
                return {
                    "status": "success",
                    "file": os.path.basename(file_path),
                    "preview": df.head().to_dict(),
                    "metadata": result.get('metadata'),
                    "tables": result.get('tables'),
                    "elapsed_sec": elapsed
                }
            except Exception as e:
                logger.exception(f"File handling exception: {e}")
                return {"status": "failed", "error": str(e)}

        # Parallel tasks
        if not topic:
            logger.warning("No topic or file provided.")
            return {"status": "failed", "reason": "No topic or file provided.", "elapsed_sec": round(time.time() - start_time, 3)}

        prompt = (
            "You're a safety and risk management expert for construction sites. "
            "Given the topic, identify:\n"
            "- Key safety hazards\n"
            "- Environmental and human factors\n"
            "- Potential risks and consequences\n"
            "- Recommended mitigations\n\n"
            f"Topic: {topic}\n\n"
            "Respond in structured bullet points."
        )
        llm = config.get("llm") if config else None

        async def llm_task():
            if llm:
                try:
                    response = await llm.complete(prompt)
                    return response.text.strip()
                except Exception as e:
                    logger.error(f"LLM error: {e}")
                    return f"[LLM error] {e}"
            return f"[Stub] Risk assessment for: {topic}"

        async def ml_task():
            try:
                features = data_input.get("ml_features")
                if features and self.ml_model:
                    df = pd.DataFrame([features])
                    prediction = int(self.ml_model.predict(df)[0])
                    logger.info(f"ML prediction: {prediction}")
                    return prediction
            except Exception as e:
                logger.error(f"ML prediction error: {e}")
                return f"ML prediction failed: {e}"
            return None

        async def rules_task():
            violations = []

            @ruleset("compliance")
            def rules():
                @rules.when_all(m.subject == "scaffolding" & (m.height > 2) & (m.has_guardrails == False))
                def missing_guardrails(c):
                    violations.append("⚠️ Guardrails missing on scaffolding over 2m.")
                @rules.when_all(m.subject == "ppe" & (m.helmet == False))
                def helmet_missing(c):
                    violations.append("⚠️ No helmet detected on worker.")
                @rules.when_all(m.subject == "fall_protection" & (m.has_harness == False))
                def missing_harness(c):
                    violations.append("⚠️ No fall protection harness detected where required.")
                @rules.when_all(m.subject == "ladder" & (m.height > 3) & (m.secured == False))
                def unsecured_ladder(c):
                    violations.append("⚠️ Ladder over 3m is not secured.")
                @rules.when_all(m.subject == "equipment" & (m.operator_certified == False))
                def uncertified_operator(c):
                    violations.append("⚠️ Heavy equipment operator is not certified.")
                @rules.when_all(m.subject == "lifting" & (m.load > m.capacity))
                def overload_lift(c):
                    violations.append("⚠️ Lifting operation exceeds equipment capacity.")
                @rules.when_all(m.subject == "chemical" & (m.has_msds == False))
                def missing_msds(c):
                    violations.append("⚠️ No MSDS (Material Safety Data Sheet) for chemical on site.")
                @rules.when_all(m.subject == "chemical" & (m.ppe == False))
                def no_chemical_ppe(c):
                    violations.append("⚠️ No PPE used for chemical handling.")
                @rules.when_all(m.subject == "electrical" & (m.lockout_tagout == False))
                def missing_lockout(c):
                    violations.append("⚠️ Lockout/Tagout procedure not followed for electrical work.")
                @rules.when_all(m.subject == "fire" & (m.extinguisher_present == False))
                def no_extinguisher(c):
                    violations.append("⚠️ No fire extinguisher present in fire risk area.")
                @rules.when_all(m.subject == "first_aid" & (m.kit_present == False))
                def no_first_aid_kit(c):
                    violations.append("⚠️ No first aid kit available on site.")
                @rules.when_all(m.subject == "noise" & (m.db_level > 85) & (m.hearing_protection == False))
                def no_hearing_protection(c):
                    violations.append("⚠️ Hearing protection not used in high noise area.")
                @rules.when_all(m.subject == "respiratory" & (m.dust_level > 0.1) & (m.mask == False))
                def no_mask(c):
                    violations.append("⚠️ Respiratory mask not used in dusty environment.")
                @rules.when_all(m.subject == "behavior" & (m.unsafe_act == True))
                def unsafe_behavior(c):
                    violations.append("⚠️ Unsafe behavior observed. Immediate intervention required.")

            for item in data_input.get("rule_checks", []):
                try:
                    post("compliance", item)
                except Exception as e:
                    logger.error(f"Rule engine error: {e}")
                    violations.append(f"Rule engine error: {e}")
            return violations

        risk_assessment_text, ml_risk_level, violations = await asyncio.gather(
            llm_task(), ml_task(), rules_task()
        )

        elapsed = round(time.time() - start_time, 3)
        logger.info(f"Completed risk assessment in {elapsed}s")

        return {
            "status": "success",
            "topic": topic,
            "risk_assessment": risk_assessment_text,
            "ml_risk_prediction": ml_risk_level,
            "violations": violations,
            "elapsed_sec": elapsed
        }

def get_agent():
    return RiskAssessmentAgent()

