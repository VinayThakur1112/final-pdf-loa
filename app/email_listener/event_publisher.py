import json
import os
from google.cloud import pubsub_v1

PROJECT_ID = os.getenv("GCP_PROJECT_ID")
TOPIC_ID = os.getenv("PUBSUB_TOPIC")

publisher = pubsub_v1.PublisherClient()
topic_path = publisher.topic_path(PROJECT_ID, TOPIC_ID)

def publish_event(event: dict):
    # event["published_at"] = time.time()
    # print("📤 EVENT:", json.dumps(event, indent=2))

    data = json.dumps(event).encode("utf-8")
    publisher.publish(topic_path, data)
    print("📤 Published event to Pub/Sub")