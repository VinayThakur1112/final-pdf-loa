import time
from app.email_listener.mail_client import (
    connect,
    wait_for_new_mail,
    fetch_unseen,
    read_message,
)

def listen():
    server = connect()
    print("📬 Email listener started...")

    while True:
        responses = wait_for_new_mail(server)
        if not responses:
            continue

        for uid in fetch_unseen(server):
            msg = read_message(server, uid)

            print("📧 New email received")
            print("Subject:", msg.get_subject())
            print("From:", msg.get_addresses("from"))

            for part in msg.mailparts:
                if part.filename:
                    print("📎 Attachment found:", part.filename)

        time.sleep(1)