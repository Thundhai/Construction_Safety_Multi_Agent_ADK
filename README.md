
## Tech_AI_Team: AI Agents for Construction Safety Content & Compliance

Overview

Tech_AI_Team is a multi-agent system built with Google’s Agent Development Kit (ADK) to enhance construction site safety using AI. It automates content generation, ensures regulatory compliance, and can extend to generate multilingual voice-over scripts. This project was developed for the Google Cloud Multi-Agent Hackathon 2024

 Key Use Case

Our system ingests incident and observation reports from construction sites and produces:

-  OSHA/ISO-compliant safety content (e.g., Instagram posts, scripts)
-  Context-aware voice-over scripts
-  Insights for training and behavioral reinforcement
-  Content reviewed for global regulatory compliance

## Agents in Action

| Agent     |  Capabilities|Notes  |
|DataEngineerAgent|------------------------------------------------------------------------------|-----------------------------------------------------------------------|
| ContentCreationAgent | Creates social media posts, captions, training texts| Focused on safety awareness (e.g., hand injuries, forklift risks) |
| ComplianceCheckerAgent | Reviews content against OSHA, ISO, UK-HSE, EU, China safety standards    | Flags non-compliance, ensures prevention-focused tone  |
| VoiceOverAgent  | Converts safety messages into scripts for narration | Tone: calm, clear, instructional  |
| DataStreamer | Simulates real-time construction site reports | Sends structured task events into the ADK environment |

## Example Scenario

Input Incident:
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

## Output (Instagram Post + Script):
- Image/Video:Proper glove usage with box cutters
- Caption:
> Hand Safety Alert!  25% rise in hand lacerations—mostly involving box cutters! Always wear cut-resistant gloves. 
>
> #HandSafety #ConstructionSafety #PPE

- Voiceover Script:
> Working with box cutters? Protect your hands! Data shows lacerations are on the rise. Wear gloves. Work safe.

---

## Tech Stack

-  Google ADK (Agent Development Kit)
-  Python (agents & simulations)
-  Google Cloud Pub/Sub (for messaging)
-  JSON for task input schema
-  Content generated is suitable for platforms like Instagram and TikTok

---

##  Diagram

![Flowchart](A_flowchart-style_digital_illustration_depicts_an_.png)

---

## How to Run Locally

1. Clone this repo:
```bash
git clone https://github.com/Thundhai/tech_ai_team_adk.git
cd tech_ai_team_adk
```

2. Set up the Python environment:
```bash
pip install -r requirements.txt
```

3. Run the data streamer:
```bash
cd content_creation_agent
python data_streamer.py
```

4. Watch the ADK system handle simulated inputs and generate output files (e.g., `output/`).

---

##  Compliance Considerations

- No depiction of real injuries
- All scenarios use hypothetical or anonymized data
- Legal and policy review guidelines included
- Multilingual and voice output compliant with privacy standards

---

##  Extensibility

Planned or potential future features:

-  Multilingual support
-  Real-time voice narration
-  Live IoT data integration from construction sites
-  On-device agents for remote locations

---

## Agent Limitations

| Agent            | Limitations                                                  |
|--------------------- |----------------------------------------------------------------------------|
| Content Agent        | May produce repetitive or generic content                     |
| Compliance Checker   | Cannot give legal advice; flags only based on known rules     |
| Voice Agent          | Cannot speak in real-time; output only scripted               |
| DataStreamer         | Simulated data; not live unless integrated with real sensors  |

---

##  Submission for Hackathon

Challenge: Automate a real-world process using multi-agent systems  
Our Solution: Smart, compliant, content automation for construction safety  
Team: Solo (Babatunde Adedigba)  
GitHub: [GitHub Repo](https://github.com/Thundhai/tech_ai_team_adk)

---

##  Contact

Created by Babatunde Adedigba 
