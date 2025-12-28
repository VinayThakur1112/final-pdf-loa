from datetime import datetime, timezone
from app.gcp.storage import upload_pdf_with_metadata
import uuid
from app.common.logging import get_logger
logger = get_logger(__name__)


BUCKET_NAME = "dit-final-pdf-loa-datalake"


def build_object_path(filename: str) -> str:
    now = datetime.now(timezone.utc)
    return (
        f"invoices/"
        f"{now.year}/{now.month:02d}/{now.day:02d}/"
        f"{filename}"
    )


def upload_invoice_pdf(
        pdf_bytes: bytes, filename: str, mail_message_id: str,
        tid: str):
    
    logger.info(f"Uploading PDF to GCS bucket: {BUCKET_NAME}")
    object_name = build_object_path(filename)

    metadata = {
        "pipeline": "final-pdf-loa",
        "source": "mail",
        "status": "unprocessed",
        "received_ts": datetime.now(timezone.utc).isoformat(),
        "message_id": mail_message_id,
        "version": "1",
        "tid": tid,
    }

    upload_pdf_with_metadata(
        bucket_name=BUCKET_NAME,
        object_name=object_name,
        content=pdf_bytes,
        metadata=metadata,
    )

    logger.info(f"Uploaded PDF as gs://{BUCKET_NAME}/{object_name}")
    return {
        "bucket": BUCKET_NAME,
        "object": object_name,
    }