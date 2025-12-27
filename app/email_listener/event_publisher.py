import json
import os
from google.cloud import pubsub_v1
from app.common.logging import get_logger
logger = get_logger(__name__)

PROJECT_ID = os.getenv("GCP_PROJECT_ID")
TOPIC_ID = os.getenv("PUBSUB_TOPIC")

publisher = pubsub_v1.PublisherClient()
topic_path = publisher.topic_path(PROJECT_ID, TOPIC_ID)

def publish_event(event: dict):
    logger.info("Publishing event to Pub/Sub")
    # event["published_at"] = time.time()
    # print("📤 EVENT:", json.dumps(event, indent=2))

    data = json.dumps(event).encode("utf-8")
    publisher.publish(topic_path, data)
    logger.info("Event published successfully")