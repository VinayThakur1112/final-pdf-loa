from app.pdf_processor.parser import parse_invoice
import json

def process_pdf(event: dict):
    pdf_path = event["file_path"]
    tid = event.get("tid")

    invoice = parse_invoice(pdf_path, tid)

    print("📄 Invoice Parsed Successfully")
    print(json.dumps(invoice.__dict__, indent=2, default=str))

    return invoice