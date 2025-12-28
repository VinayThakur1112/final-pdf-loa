import time
import time
import re
import os

from app.email_listener.mail_client import (
    connect,
    wait_for_new_mail,
    fetch_unseen,
    read_message,
)
from app.email_listener.downloader import download_pdf
from app.email_listener.event_publisher import publish_event
from app.email_listener.uploader import upload_invoice_pdf
from app.common.logging import get_logger
logger = get_logger(__name__)


def get_tid(subject: str) -> str:
    logger.info(f"Extracting TID from subject: {subject}")
    pattern = r'\b([a-zA-Z0-9]{4}(?:-[a-zA-Z0-9]{4}){3})\b'
    match = re.search(pattern, subject)

    if match:
        tid = match.group(1)
        logger.info(f"TID: {tid}")
        return tid
    else:
        logger.warning("No TID found")
        return "unknown"


def listen():
    logger.info("Connecting to mail server...")
    server = connect()
    logger.info("📬 Email listener started...")

    while True:
        responses = wait_for_new_mail(server)
        if not responses:
            continue

        for uid in fetch_unseen(server):
            logger.info(f"Processing email UID: {uid}")
            msg = read_message(server, uid)

            tid = get_tid(msg.get_subject())

            for part in msg.mailparts:
                if not part.filename:
                    continue

                file_path = download_pdf(part, tid)
                if not file_path:
                    continue
                logger.info(f"Downloaded attachment to: {file_path}")

                # print(type(part))
                # print(dir(part))
                pdf_bytes = part.get_payload()
                upload_result = upload_invoice_pdf(
                    pdf_bytes, 
                    os.path.basename(file_path), 
                    msg.get('message-id'),
                    tid
                )
                logger.info(f"Uploaded PDF from attachment: {part.filename}")

                event = {
                    "source": "email",
                    "file_path": file_path,
                    "filename": os.path.basename(file_path),
                    "tid": tid,
                    "bucket": upload_result["bucket"],
                    "object": upload_result["object"],
                }

                publish_event(event)

        time.sleep(1)