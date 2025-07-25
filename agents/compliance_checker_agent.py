from adk_local import RuntimeContext
from adk_local import Agent  # optionally alias Agent if needed


class ComplianceCheckerAgent(Agent):
    def __init__(self):
        super().__init__(
            name="ComplianceCheckerAgent",
            description="Checks text for compliance with global safety standards using LLM or rule-based logic.",
            model="gemini-2.0-pro"
        )

    async def run(self, context: RuntimeContext) -> None:
        import time
        import asyncio
        from utils.advanced_data_loader import load_data
        from utils.standards_updater import get_latest_standards
        start_time = time.time()

        # Support both file and text input
        content = context.input
        files = getattr(context, 'files', []) if hasattr(context, 'files') else []
        # Option to force-refresh standards (e.g., context.force_refresh_standards = True)
        force_refresh = getattr(context, 'force_refresh_standards', False)
        # Get latest standards (online or cached)
        standards_dict = get_latest_standards(force_refresh=force_refresh)
        standards = list(standards_dict.keys())

        # Load file if present
        file_text = None
        file_metadata = None
        if files and len(files) > 0:
            file_path = files[0]
            result = load_data(file_path)
            if 'error' in result:
                context.complete({
                    "status": "failed",
                    "reason": result['error'],
                    "recommendations": [],
                    "violated_standards": [],
                    "elapsed_sec": round(time.time() - start_time, 3)
                })
                return
            file_text = result['data'].to_string(index=False) if hasattr(result['data'], 'to_string') else str(result['data'])
            file_metadata = result.get('metadata')
            content = file_text

        if not content:
            context.logger.warning("[ComplianceCheckerAgent] No text or file provided for compliance checking.")
            context.complete({
                "status": "failed",
                "compliance": "non-compliant",
                "reason": "No text or file provided.",
                "recommendations": [],
                "violated_standards": [],
                "elapsed_sec": round(time.time() - start_time, 3)
            })
            return

        context.logger.info(f"[ComplianceCheckerAgent] Checking content for compliance. Standards used: {standards}")

        # Section-by-section analysis
        def split_sections(text):
            # Split by paragraphs or headings (customize as needed)
            import re
            sections = re.split(r'\n{2,}|(?m)^#+ ', text)
            return [s.strip() for s in sections if s.strip()]

        llm = getattr(context, 'llm', None)

        async def llm_task(section_text):
            if llm and hasattr(llm, 'complete'):
                try:
                    prompt = (
                        f"You're a safety compliance expert. Analyze the following section for alignment with these standards: {', '.join(standards)}. "
                        "Identify violations, cite specific standards, and suggest improvements.\n\n"
                        f"Section:\n{section_text}"
                    )
                    llm_response = await llm.complete(prompt)
                    return llm_response.text.strip()
                except Exception as e:
                    return f"[LLM error] {e}"
            return "[Stub] Compliance check. No LLM available."

        async def rules_task(section_text):
            violations = []
            recommendations = []
            violated_standards = []
            text = section_text.lower()
            # 1. Standards reference check (existing)
            for std in standards:
                if std.lower() not in text:
                    violations.append(f"No {std} reference found.")
                    recommendations.append(f"Include {std} requirements in documentation.")
                    violated_standards.append(std)

            # 2. Required safety keywords
            required_keywords = ["ppe", "hazard", "training", "incident", "risk", "emergency", "supervisor", "reporting"]
            for kw in required_keywords:
                if kw not in text:
                    violations.append(f"Missing required keyword: '{kw}'.")
                    recommendations.append(f"Mention '{kw}' where relevant.")

            # 3. Vague language detection
            vague_terms = ["should", "may", "could", "as appropriate", "if possible"]
            for vt in vague_terms:
                if vt in text:
                    violations.append(f"Vague language detected: '{vt}'.")
                    recommendations.append(f"Use stronger compliance language instead of '{vt}' (e.g., 'must', 'shall').")

            # 4. Section completeness: check for required subtopics
            required_subtopics = ["responsible", "procedure", "review", "frequency"]
            for sub in required_subtopics:
                if sub not in text:
                    violations.append(f"Section may be missing required subtopic: '{sub}'.")
                    recommendations.append(f"Ensure '{sub}' is addressed in this section.")

            # 5. Role/responsibility assignment
            if not any(role in text for role in ["officer", "supervisor", "manager", "employee", "worker"]):
                violations.append("No clear role or responsibility assigned.")
                recommendations.append("Assign clear roles (e.g., 'Safety Officer', 'Supervisor') for each procedure.")

            # 6. Actionability: flag passive/unclear instructions
            passive_terms = ["will be", "should be", "can be", "is to be"]
            for pt in passive_terms:
                if pt in text:
                    violations.append(f"Passive/unclear instruction: '{pt}'.")
                    recommendations.append(f"Use actionable, direct instructions instead of '{pt}'.")

            # 7. Section length check
            if len(section_text.split()) < 20:
                violations.append("Section is very short; may lack detail.")
                recommendations.append("Expand section to provide sufficient detail for compliance.")
            if len(section_text.split()) > 400:
                violations.append("Section is very long; may be hard to follow.")
                recommendations.append("Consider splitting into smaller, focused sections.")

            return violations, recommendations, violated_standards

        # Analyze each section
        sections = split_sections(content)
        tasks = []
        for section in sections:
            tasks.append(asyncio.gather(llm_task(section), rules_task(section)))
        section_outputs = await asyncio.gather(*tasks)

        # Aggregate results
        all_violations = []
        all_recommendations = []
        all_violated_standards = []
        section_breakdown = []
        for i, (assessment, (violations, recommendations, violated_standards)) in enumerate(section_outputs):
            section_breakdown.append({
                "section": i+1,
                "text": sections[i],
                "assessment": assessment,
                "violations": violations,
                "recommendations": recommendations,
                "violated_standards": violated_standards
            })
            all_violations.extend(violations)
            all_recommendations.extend(recommendations)
            all_violated_standards.extend(violated_standards)

        elapsed = round(time.time() - start_time, 3)
        context.complete({
            "status": "success",
            "section_breakdown": section_breakdown,
            "violations": all_violations,
            "recommendations": all_recommendations,
            "violated_standards": list(set(all_violated_standards)),
            "file_metadata": file_metadata,
            "elapsed_sec": elapsed,
            "standards_used": standards_dict
        })

# ✅ For ADK CLI execution
async def run_with_adk(task: dict) -> dict:
    agent = ComplianceCheckerAgent()
    return await agent.run_with_adk(task)

def get_agent():
    return ComplianceCheckerAgent()
