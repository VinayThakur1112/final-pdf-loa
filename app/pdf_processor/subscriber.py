import json
import os
from google.cloud import pubsub_v1
from app.pdf_processor.processor import process_pdf
from app.common.logging import get_logger
logger = get_logger(__name__)

PROJECT_ID = os.getenv("GCP_PROJECT_ID")
SUBSCRIPTION_ID = os.getenv("PUBSUB_SUBSCRIPTION")

subscriber = pubsub_v1.SubscriberClient()
subscription_path = subscriber.subscription_path(
    PROJECT_ID, SUBSCRIPTION_ID
)

def callback(message):
    try:
        event = json.loads(message.data.decode("utf-8"))
        logger.info(f"event: {event}")
        process_pdf(event)
        message.ack()
        logger.info("✅ Message processed & acknowledged")
    except Exception as e:
        logger.error("❌ Processing failed:", e)
        message.nack()

def start_subscriber():
    logger.info("📡 PDF Processor subscriber started...")
    streaming_pull = subscriber.subscribe(
        subscription_path, callback=callback
    )
    
    streaming_pull.result()
    logger.info("🛑 PDF Processor subscriber completed.")