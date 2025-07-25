from google.adk import Agent

from datetime import datetime
import sqlite3
import os

class TrainingComplianceAgent(Agent):
    def __init__(self):
        super().__init__(
            name="TrainingComplianceAgent",
            description="Recommends personalized training, checks certifications, and integrates with LearningAnalyticsAgent.",
            model="gemini-2.0-pro"
        )
        self.db_path = "data/training.db"
        os.makedirs("data", exist_ok=True)
        self._init_db()

    def _init_db(self):
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS training_records (
                    worker_id TEXT,
                    name TEXT,
                    role TEXT,
                    cert_type TEXT,
                    issued_date TEXT,
                    expiry_date TEXT
                )
            """)
            conn.commit()

    async def run(self, context) -> None:
        task = context.task
        # Advanced loader
        from utils.advanced_data_loader import load_data
        if isinstance(task, str):
            result = load_data(task)
            if 'error' in result:
                context.complete({'error': result['error']})
                return
            df = result['data']
            context.logger.info(f"Loaded file for training compliance: {task}, shape: {df.shape}")
            context.complete({"file_preview": df.head().to_dict(), "metadata": result.get('metadata'), "tables": result.get('tables')})
            return
        # CSV support
        if isinstance(task, str) and task.endswith('.csv'):
            import os
            import pandas as pd
            file_path = os.path.join('data', task) if not os.path.isabs(task) else task
            if os.path.exists(file_path):
                df = pd.read_csv(file_path)
                context.logger.info(f"Loaded CSV for training compliance: {file_path}, shape: {df.shape}")
                context.complete({"csv_preview": df.head().to_dict()})
                return
        role = task.get("role")
        experience = task.get("experience_years", 0)
        gaps = task.get("skill_gaps", [])

        if not role:
            context.complete({"status": "failed", "reason": "No role provided."})
            return

        context.logger.info("📚 Recommending training and checking certifications...")

        # 1. Recommend Training
        training_map = {
            "scaffolding": ["Fall prevention basics", "Scaffold erection training"],
            "ppe": ["Proper PPE usage", "Heat safety awareness"],
            "electrical": ["Lockout/Tagout (LOTO)", "Arc flash awareness"],
            "general": ["Hazard identification", "Site orientation"]
        }

        recommended = set()
        for gap in gaps:
            recommended.update(training_map.get(gap, []))
        if experience < 2:
            recommended.update(["Basic safety induction", "Mentorship program"])

        recommended = list(recommended)

        # 2. Check Expiring Certifications
        expired = []
        with sqlite3.connect(self.db_path) as conn:
            rows = conn.execute("""
                SELECT name, cert_type, expiry_date FROM training_records
                WHERE expiry_date < ?
            """, (datetime.now().strftime("%Y-%m-%d"),)).fetchall()
            for row in rows:
                expired.append({
                    "name": row[0],
                    "certification": row[1],
                    "expired_on": row[2]
                })

        # 3. Summary to share with LearningAnalyticsAgent
        summary = {
            "role": role,
            "recommended_training": recommended,
            "expired_certifications": expired,
            "skill_gaps": gaps
        }

        # 4. Optional call to LearningAnalyticsAgent
        try:
            response = await context.call("learning_analytics_agent", {
                "linked_output": str(summary),
                "from_agent": "training_compliance_agent"
            })
            insights = response.output.get("insights", "No insights returned.")
        except Exception as e:
            context.logger.warning(f"⚠️ Could not call learning_analytics_agent: {str(e)}")
            insights = "N/A"

        # 5. Complete
        context.complete({
            "status": "success",
            "role": role,
            "recommended_training": recommended,
            "expired_certifications": expired,
            "learning_insights": insights
        })

async def run_with_adk(task: dict) -> dict:
    agent = TrainingComplianceAgent()
    return await agent.run_with_adk(task)

def get_agent():
    return TrainingComplianceAgent()

