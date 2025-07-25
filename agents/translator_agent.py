from google.adk import Agent


class TranslationAgent(Agent):
    def __init__(self):
        super().__init__(
            name="TranslationAgent",
            description="Translates construction safety and operations instructions into multiple local and international languages.",
            model="gemini-2.0-pro"
        )

    async def run(self, context) -> None:
        content = context.input
        # Advanced loader
        from utils.advanced_data_loader import load_data
        if isinstance(content, str):
            result = load_data(content)
            if 'error' in result:
                context.complete({'error': result['error']})
                return
            df = result['data']
            context.logger.info(f"Loaded file for translation: {content}, shape: {df.shape}")
            translated = df.iloc[:,0].apply(lambda x: f"[translated] {x}")
            context.complete({"translated": translated.tolist(), "metadata": result.get('metadata'), "tables": result.get('tables')})
            return
        # CSV support
        if isinstance(content, str) and content.endswith('.csv'):
            import os
            import pandas as pd
            file_path = os.path.join('data', content) if not os.path.isabs(content) else content
            if os.path.exists(file_path):
                df = pd.read_csv(file_path)
                context.logger.info(f"Loaded CSV for translation: {file_path}, shape: {df.shape}")
                # Example: translate first column
                translated = df.iloc[:,0].apply(lambda x: f"[translated] {x}")
                context.complete({"translated": translated.tolist()})
                return
        context.logger.info("[TranslationAgent] Translating construction or operational instruction.")

        if not content:
            context.complete({
                "status": "failed",
                "reason": "No construction/operations content provided."
            })
            return

        if hasattr(context.llm, 'complete'):
            prompt = (
                "You are a professional translator specializing in translating critical construction and field operations instructions "
                "into local African and international languages, ensuring clarity, accuracy, and tone suitable for workers on construction sites. "
                "Translate the following safety or operational instruction into:\n"
                "- French\n"
                "- Spanish\n"
                "- Arabic\n"
                "- Hausa (Nigeria)\n"
                "- Yoruba (Nigeria)\n"
                "- Swahili (East Africa)\n"
                "- Zulu (South Africa)\n"
                "- Igbo (Nigeria)\n"
                "- Portuguese (Mozambique, Angola)\n"
                "- Amharic (Ethiopia)\n\n"
                f"Text:\n{content}"
            )
            result = await context.llm.complete(prompt)
            translations = result.text.strip()
        else:
            translations = {
                "French": f"[Stub] French: {content}",
                "Spanish": f"[Stub] Spanish: {content}",
                "Arabic": f"[Stub] Arabic: {content}",
                "Hausa": f"[Stub] Hausa: {content}",
                "Yoruba": f"[Stub] Yoruba: {content}",
                "Swahili": f"[Stub] Swahili: {content}",
                "Zulu": f"[Stub] Zulu: {content}",
                "Igbo": f"[Stub] Igbo: {content}",
                "Portuguese": f"[Stub] Portuguese: {content}",
                "Amharic": f"[Stub] Amharic: {content}"
            }

        context.complete({
            "status": "success",
            "translations": translations
        })

async def run_with_adk(task: dict) -> dict:
    agent = TranslationAgent()
    return await agent.run_with_adk(task)

def get_agent():
    return TranslationAgent()
