import json
import os
from google.cloud import pubsub_v1
from app.pdf_processor.processor import process_pdf

PROJECT_ID = os.getenv("GCP_PROJECT_ID")
SUBSCRIPTION_ID = os.getenv("PUBSUB_SUBSCRIPTION")

subscriber = pubsub_v1.SubscriberClient()
subscription_path = subscriber.subscription_path(
    PROJECT_ID, SUBSCRIPTION_ID
)

def callback(message):
    try:
        event = json.loads(message.data.decode("utf-8"))
        process_pdf(event)
        message.ack()
        print("✅ Message processed & acknowledged")
    except Exception as e:
        print("❌ Processing failed:", e)
        message.nack()

def start_subscriber():
    print("📡 PDF Processor subscriber started...")
    streaming_pull = subscriber.subscribe(
        subscription_path, callback=callback
    )
    
    streaming_pull.result()