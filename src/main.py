import logging
import json
import os
from src.db import init_db, ExtractedData
from src.email_client import EmailClient
from src.pdf_parser import PDFParser

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def main():
    logger.info("Starting PDF Extraction Pipeline")
    
    # 1. Initialize DB
    session = init_db()
    logger.info("Database initialized")

    # 2. Initialize Clients
    email_client = EmailClient()
    pdf_parser = PDFParser()

    # 3. Fetch Emails
    logger.info("Fetching emails...")
    messages = email_client.fetch_emails()
    
    if not messages:
        logger.info("No new emails found.")
        return

    for msg in messages:
        msg_id = msg['id']
        logger.info(f"Processing email {msg_id}")
        
        # Get metadata
        details = email_client.get_email_details(msg_id)
        subject = ''
        sender = ''
        if details:
            headers = details['payload']['headers']
            subject = next((h['value'] for h in headers if h['name'] == 'Subject'), 'No Subject')
            sender = next((h['value'] for h in headers if h['name'] == 'From'), 'Unknown')

        # 4. Download Attachments
        pdf_paths = email_client.download_attachments(msg_id)
        
        for path in pdf_paths:
            # 5. Parse PDF
            logger.info(f"Parsing PDF: {path}")
            parsed_data = pdf_parser.parse_pdf(path)
            
            if parsed_data:
                # 6. Store in DB
                try:
                    record = ExtractedData(
                        source_email_id=msg_id,
                        sender=sender,
                        subject=subject,
                        pdf_filename=os.path.basename(path),
                        extracted_text=parsed_data['text'],
                        extracted_json=json.dumps(parsed_data['tables'])
                    )
                    session.add(record)
                    session.commit()
                    logger.info(f"Stored data for parsing of {path}")
                except Exception as e:
                    logger.error(f"Failed to save record to DB: {e}")
                    session.rollback()
            
            # Cleanup
            # os.remove(path) 

    logger.info("Pipeline finished")

if __name__ == "__main__":
    main()
