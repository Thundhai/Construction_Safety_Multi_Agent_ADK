import csv
import asyncio
import json
import os
import aiohttp

ADK_ENDPOINT = "http://localhost:8000/agents/tech_ai_team_adk/invoke"

async def send_task_to_adk(payload):
    async with aiohttp.ClientSession() as session:
        async with session.post(ADK_ENDPOINT, json=payload) as resp:
            if resp.status == 200:
                result = await resp.json()
                print(f"✅ Task accepted. Result: {json.dumps(result, indent=2)}")
            else:
                print(f"❌ Failed with status {resp.status}")
                print(await resp.text())

async def stream_data_from_csv(csv_path):
    if not os.path.exists(csv_path):
        print(f"❌ File not found: {csv_path}")
        return

    with open(csv_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            task_payload = {
                "input": row.get("description", "No description provided")
            }

            print(f"🛰️ Sending Task:\n{json.dumps(task_payload, indent=2)}")
            await send_task_to_adk(task_payload)
            await asyncio.sleep(1)  # Optional delay

if __name__ == "__main__":
    csv_path = "sample_tasks.csv"
    asyncio.run(stream_data_from_csv(csv_path))
