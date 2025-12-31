from sys import argv

if __name__ == "__main__":
    
    if argv[1] == "email_listener":
        from app.email_listener.listener import listen
        try:
            listen()
        except KeyboardInterrupt:
            print("📪 Email listener stopped by user")
            
    elif argv[1] == "pdf_processor":
        from app.pdf_processor.subscriber import start_subscriber
        try:
            start_subscriber()
        except KeyboardInterrupt:
            print("📄 PDF processor subscriber stopped by user")
    
    elif argv[1] == "customer_data":
        from app.customer_data.load_data_bq import push_customer_data
        try:
            push_customer_data()
        except KeyboardInterrupt:
            print("📄 Customer data subscriber stopped by user")