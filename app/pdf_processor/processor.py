from app.pdf_processor.parser import parse_invoice
from app.db.repository import save_invoice
from app.gcp.storage import (
    download_pdf,
    get_metadata,
    update_metadata,
)
from app.common.logging import get_logger
import tempfile
from datetime import datetime
import json

logger = get_logger(__name__)


def process_pdf(event: dict):
    logger.info("📄 Processing PDF event...")

    bucket = event["bucket"]
    object_name = event["object"]
    tid = event.get("tid")

    # 1️⃣ Idempotency check
    metadata = get_metadata(bucket, object_name)
    logger.info(f"PDF Metadata: {metadata}")
    
    if metadata.get("status") != "unprocessed":
        logger.info("⚠️ PDF already processed. Skipping.")
        logger.info(metadata.get("status"))
        return None

    try:
        # 2️⃣ Download PDF from GCS
        pdf_bytes = download_pdf(bucket, object_name)

        # 3️⃣ Parse PDF (using temp file)
        with tempfile.NamedTemporaryFile(suffix=".pdf") as tmp:
            tmp.write(pdf_bytes)
            tmp.flush()

            invoice = parse_invoice(tmp.name, tid)

        # 4️⃣ Save to DB
        save_invoice(invoice)

        # 5️⃣ Update metadata → processed
        update_metadata(
            bucket,
            object_name,
            {
                "status": "processed",
                "processed_ts": datetime.now().isoformat(),
            },
        )

        logger.info("📄 Invoice Parsed Successfully")
        logger.info(json.dumps(invoice.__dict__, indent=2, default=str))

        return invoice

    except Exception as exc:
        # 6️⃣ Update metadata → failed
        update_metadata(
            bucket,
            object_name,
            {
                "status": "failed",
                "error": str(exc)[:1024],
                "failed_ts": datetime.now().isoformat(),
            },
        )

        logger.exception("❌ PDF processing failed")
        raise