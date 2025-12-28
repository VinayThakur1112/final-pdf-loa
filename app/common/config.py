import os
from dotenv import load_dotenv


load_dotenv()

MAIL_HOST = os.getenv("MAIL_HOST")
MAIL_PORT = int(os.getenv("MAIL_PORT"))
MAIL_USER = os.getenv("MAIL_USER")
MAIL_PASSWORD = os.getenv("MAIL_PASSWORD")
MAIL_FOLDER = os.getenv("MAIL_FOLDER", "INBOX")