from imapclient import IMAPClient
import pyzmail
from app.common.config import (
    MAIL_HOST,
    MAIL_PORT,
    MAIL_USER,
    MAIL_PASSWORD,
    MAIL_FOLDER,
)

def connect():
    server = IMAPClient(MAIL_HOST, port=MAIL_PORT, ssl=True)
    server.login(MAIL_USER, MAIL_PASSWORD)
    server.select_folder(MAIL_FOLDER)
    return server

def wait_for_new_mail(server, timeout=300):
    server.idle()
    responses = server.idle_check(timeout=timeout)
    server.idle_done()
    return responses

def fetch_unseen(server):
    return server.search(["UNSEEN"])

def read_message(server, uid):
    raw = server.fetch(uid, ["BODY[]"])
    return pyzmail.PyzMessage.factory(raw[uid][b"BODY[]"])