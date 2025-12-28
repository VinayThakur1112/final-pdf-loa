import pdfplumber
import re
from app.pdf_processor.schema import Invoice, InvoiceItem
from app.common.logging import get_logger
logger = get_logger(__name__)

def parse_invoice(pdf_path: str, tid: str) -> Invoice:
    logger.info(f"Parsing invoice PDF: {pdf_path}")
    with pdfplumber.open(pdf_path) as pdf:
        text = "\n".join(page.extract_text() for page in pdf.pages)

    invoice_id = _extract_invoice_id(text)
    issue_date = _extract_issue_date(text)
    total_due = _extract_total_due(text)
    items = _extract_items(pdf_path, tid)
    
    logger.info(f"Extracted Invoice ID: {invoice_id}, \
                Issue Date: {issue_date}, \
                Total Due: {total_due}, \
                Items Count: {len(items)}")

    return Invoice(
        tid= tid,
        invoice_id=invoice_id,
        issue_date=issue_date,
        total_due=total_due,
        items=items
    )

def _extract_invoice_id(text):
    match = re.search(r"Invoice#\s+(\S+)", text)
    return match.group(1) if match else None

def _extract_issue_date(text):
    match = re.search(r"Issue date\s+(\d{2}-\d{2}-\d{4})", text)
    return match.group(1) if match else None

def _extract_total_due(text):
    match = re.search(r"Total Due\s+\$(\d+\.?\d*)", text)
    return float(match.group(1)) if match else None

def _extract_items(pdf_path, tid):
    items = []

    with pdfplumber.open(pdf_path) as pdf:
        table = pdf.pages[0].extract_table()

    if not table:
        return items

    headers = table[0]
    rows = table[1:]

    for row in rows:
        try:
            item = InvoiceItem(
                tid=tid,
                item_name=row[0],
                qty=int(row[1]),
                rate=float(row[2]),
                amount=float(row[3].replace("$", "")),
            )
            items.append(item)
        except Exception:
            continue

    return items