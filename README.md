
# Tech_AI_Team: AI Agents for Construction Safety Content & Compliance

## Overview

Tech_AI_Team is a multi-agent system built with Google’s Agent Development Kit (ADK) to enhance construction site safety using AI. It automates content generation, ensures regulatory compliance, adapts content for global audiences, performs safety risk assessments, and can even produce voice-over scripts. This project was developed for the **Google Cloud Multi-Agent Hackathon 2024**.

---

## 🔧 Key Use Case

Our system ingests incident and observation reports from construction sites and produces:

- OSHA/ISO-compliant safety content (e.g., Instagram posts, scripts)
- Context-aware voice-over scripts
- Cultural-localized safety messaging
- Safety risk assessments
- Usability feedback
- Learning analytics based on worker interaction
- Content reviewed for regulatory compliance and tone

---

## 🤖 Agents in Action

| Agent                     | Capabilities                                                                 | Notes                                                                                  |
|--------------------------|------------------------------------------------------------------------------|----------------------------------------------------------------------------------------|
| DataEngineerAgent        | Simulates incoming safety content from structured data feeds                  | Feeds task queue for the orchestrator                                                  |
| ContentCreationAgent     | Creates social media posts, captions, training texts                         | Focused on safety awareness (e.g., hand injuries, forklift risks)                     |
| ComplianceCheckerAgent   | Reviews content for OSHA, ISO, UK-HSE, EU, and China safety standards         | Flags non-compliance and ensures prevention-focused tone                              |
| VoiceOverAgent           | Converts safety messages into narration scripts                              | Tone: calm, clear, instructional                                                       |
| TranslatorAgent          | Translates safety content into target languages                              | Spanish, French, Japanese, etc.                                                       |
| RiskAssessmentAgent      | Identifies potential hazards from content topics or scenarios                 | Ensures critical risks are addressed early                                            |
| AudienceAnalysisAgent    | Analyzes target audience characteristics                                      | Ensures content relevance for demographics                                            |
| ContentLocalizationAgent | Adapts content to cultural norms and context                                  | More than just translation; ensures cultural fit                                       |
| UsabilityTestingAgent    | Tests content for clarity and user-friendliness                              | Provides feedback for improving readability and engagement                            |
| LearningAnalyticsAgent   | Tracks interaction data and effectiveness                                     | Reports completion rates, engagement, etc.                                             |
| StyleToneAnalysisAgent   | Checks tone/style of scripts for consistency                                  | Flags off-brand or inconsistent narration/text styles                                  |

---

## 🧪 Example Scenario

### Example Input:
```json
{
  "input_type": "content",
  "text": "Box cutter laceration due to no gloves",
  "meta": {
    "incident_type": "Injury",
    "location": "Zone A",
    "date": "2025-05-21"
  }
}
```

### Example Output:
- **Image/Video:** Proper glove usage with box cutters
- **Caption:**
> Hand Safety Alert! 25% rise in hand lacerations—mostly involving box cutters! Always wear cut-resistant gloves.  
> #HandSafety #ConstructionSafety #PPE

- **Voiceover Script:**
> Working with box cutters? Protect your hands! Data shows lacerations are on the rise. Wear gloves. Work safe.

---

## 🧪 Batch Agent Execution Example (From CSV Input)

| Agent                    | Input Task                                                                    | Output Summary                                                                                     |
|--------------------------|--------------------------------------------------------------------------------|-----------------------------------------------------------------------------------------------------|
| ContentCreationAgent     | Create an Instagram caption about hand injuries and box cutter usage          | Generated safety-themed social media caption using professional tone and platform-specific format. |
| ComplianceCheckerAgent   | Check compliance of this message with OSHA: 'No hard hat needed...'           | Compliance verified with recommendations to cite OSHA standards.                                   |
| VoiceOverAgent           | Write a voice-over script for crane safety training...                        | Narration script formatted for 30–60 seconds in a calm and clear voice.                            |
| TranslatorAgent          | Translate this instruction into French and Spanish...                         | Translations produced in both languages, following instruction wording.                            |
| RiskAssessmentAgent      | Identify safety risks in operating a mobile scaffold...                       | Risk assessment completed (stub — placeholder logic).                                               |
| AudienceAnalysisAgent    | Analyze safety training effectiveness...                                      | Audience analysis complete (stub).                                                                 |
| ContentLocalizationAgent | Adapt this safety message for workers in Japan...                             | Localization completed with cultural adaptation (stub).                                             |
| UsabilityTestingAgent    | Evaluate the usability of a digital incident report...                        | Usability feedback generated (stub).                                                                |
| LearningAnalyticsAgent   | Analyze completion data from PPE training videos...                           | Analytics performed on hypothetical completion data (stub).                                         |
| StyleToneAnalysisAgent   | Check if this message has a formal and professional tone...                   | Tone analysis completed with stub logic.                                                            |
| DataEngineerAgent        | Simulate an incoming task: 'Observation from Zone B...'                       | Message injected, but flagged as unrecognized format (expected in real-time simulations).           |

---

## 🧱 Tech Stack

- Google ADK (Agent Development Kit)
- Python (agents & simulations)
- Google Cloud Pub/Sub (for messaging)
- CSV & JSON for task input schema
- Content suitable for platforms like Instagram, TikTok, and LMS portals

---

## 📊 Architecture Diagram

![Flowchart](A_flowchart-style_digital_illustration_depicts_the.png)

---

## ▶️ How to Run Locally

1. Clone this repo:
```bash
git clone https://github.com/Thundhai/tech_ai_team_adk.git
cd tech_ai_team_adk
```

2. Set up the Python environment:
```bash
pip install -r requirements.txt
```

3. Run the ADK server:
```bash
adk api_server --port 8080
```

4. Run the batch from CSV:
```bash
python run_batch_from_csv.py
```

5. View results in:
```bash
output_responses.csv
```

---

## ✅ Compliance Considerations

- No real injuries are depicted
- All data is hypothetical or anonymized
- Legal/policy guidance is informational, not advisory
- Translations consider cultural sensitivity

---

## 🚀 Extensibility

Planned or potential features:
- Real-time narration via text-to-speech
- Live IoT data integration
- LMS integration for feedback tracking
- Custom agents for region-specific codes

---

## ⚠️ Agent Limitations

| Agent                      | Limitations                                                                 |
|---------------------------|----------------------------------------------------------------------------|
| DataEngineerAgent         | Simulated feed only; not connected to live site sensors                    |
| ContentCreationAgent      | May produce generic phrases; relies on input quality                       |
| ComplianceCheckerAgent    | Flags issues but does not provide legal certification                      |
| VoiceOverAgent            | Generates text scripts only; no real-time voice synthesis                  |
| TranslatorAgent           | Relies on LLM quality; idioms may translate poorly                         |
| RiskAssessmentAgent       | Not a full safety audit; identifies common risks from prompts              |
| AudienceAnalysisAgent     | Assumes default traits if metadata is lacking                              |
| ContentLocalizationAgent  | Cultural context limited to language model knowledge                       |
| UsabilityTestingAgent     | Simulated testing; does not include actual user interviews                 |
| LearningAnalyticsAgent    | Uses mock interaction data unless integrated with a front-end              |
| StyleToneAnalysisAgent    | Operates on heuristic rules and may misjudge nuanced tone                  |

---

## 🏆 Submission for Hackathon

- **Challenge:** Automate a real-world process using multi-agent systems
- **Solution:** Smart, compliant, content automation for construction safety
- **Team:** Solo (Babatunde Adedigba)
- **GitHub:** [https://github.com/Thundhai/tech_ai_team_adk](https://github.com/Thundhai/tech_ai_team_adk)

---

## 📬 Contact

Created by Babatunde Adedigba
