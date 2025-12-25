import time
from app.email_listener.mail_client import (
    connect,
    wait_for_new_mail,
    fetch_unseen,
    read_message,
)
from app.email_listener.downloader import download_pdf
from app.email_listener.event_publisher import publish_event
import time
import re

# todo temp setup
from app.pdf_processor.processor import process_pdf

def get_tid(subject: str) -> str:
    # import re
    pattern = r'\b([a-zA-Z0-9]{4}(?:-[a-zA-Z0-9]{4}){3})\b'
    match = re.search(pattern, subject)

    if match:
        tid = match.group(1)
        print("TID:", tid)
        return tid
    else:
        print("No TID found")
        return "unknown"


def listen():
    server = connect()
    print("📬 Email listener started...")

    while True:
        responses = wait_for_new_mail(server)
        if not responses:
            continue

        for uid in fetch_unseen(server):
            msg = read_message(server, uid)

            tid = get_tid(msg.get_subject())

            for part in msg.mailparts:
                if not part.filename:
                    continue

                file_path = download_pdf(part, tid)
                if not file_path:
                    continue

                event = {
                    "source": "email",
                    "file_path": file_path,
                    "filename": part.filename,
                    "tid": tid,
                }

                # todo temp setup
                # publish_event(event)
                process_pdf(event)
                
        time.sleep(1)