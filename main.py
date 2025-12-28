from sys import argv
from app.email_listener.listener import listen
from app.pdf_processor.subscriber import start_subscriber

if __name__ == "__main__":
    
    if argv[1] == "email_listener":
        listen()
    elif argv[1] == "pdf_processor":
        start_subscriber()