from app.pdf_processor.parser import parse_invoice
from app.db.repository import save_invoice
import json
from app.common.logging import get_logger
logger = get_logger(__name__)

def process_pdf(event: dict):
    logger.info("📄 Processing PDF event...")
    pdf_path = event["file_path"]
    tid = event.get("tid")

    invoice = parse_invoice(pdf_path, tid)
    save_invoice(invoice)

    logger.info("📄 Invoice Parsed Successfully")
    logger.info(json.dumps(invoice.__dict__, indent=2, default=str))

    return invoice