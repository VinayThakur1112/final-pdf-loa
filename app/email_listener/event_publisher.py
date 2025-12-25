import json
import time

def publish_event(event: dict):
    event["published_at"] = time.time()
    print("📤 EVENT:", json.dumps(event, indent=2))