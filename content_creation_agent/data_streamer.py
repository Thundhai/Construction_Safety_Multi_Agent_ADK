import csv
import asyncio
import json
import os

from google.cloud import pubsub_v1

# Replace with your topic name if using real Pub/Sub
PROJECT_ID = os.getenv("GCP_PROJECT_ID", "your-project-id")
TOPIC_ID = os.getenv("ADK_TOPIC_ID", "agent-tasks")

# If using local simulation, you can just print the payload instead of sending
USE_SIMULATION = True  # Set to False when integrating with actual ADK Pub/Sub

async def stream_data_from_csv(csv_path):
    if not os.path.exists(csv_path):
        print(f"❌ File not found: {csv_path}")
        return

    with open(csv_path, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            task_payload = {
                "input_type": "content",  # or "data"
                "text": row.get("description", "No description found"),
                "meta": {k: v for k, v in row.items() if k != "description"},
            }

            message_json = json.dumps(task_payload)

            if USE_SIMULATION:
                print(f"🛰️ Simulated Task: {message_json}")
            else:
                await publish_task_to_pubsub(message_json)

            await asyncio.sleep(0.5)  # Optional delay between tasks

async def publish_task_to_pubsub(message_json: str):
    publisher = pubsub_v1.PublisherClient()
    topic_path = publisher.topic_path(PROJECT_ID, TOPIC_ID)
    future = publisher.publish(topic_path, data=message_json.encode("utf-8"))
    print(f"✅ Published task: {future.result()}")

# Example usage
if __name__ == "__main__":
    csv_path = "sample_tasks.csv"  # Make sure to place this CSV in the same folder
    asyncio.run(stream_data_from_csv(csv_path))
