from google.cloud import storage
from typing import Dict
from app.common.logging import get_logger
logger = get_logger(__name__)

_client = storage.Client()


def upload_pdf_with_metadata(
    bucket_name: str,
    object_name: str,
    content: bytes,
    metadata: Dict[str, str],
):
    logger.info(f"Uploading PDF to GCS bucket: {bucket_name}")
    bucket = _client.bucket(bucket_name)
    blob = bucket.blob(object_name)

    blob.metadata = metadata
    blob.upload_from_string(
        content,
        content_type="application/pdf"
    )

    return blob.public_url


def download_pdf(bucket_name: str, object_name: str) -> bytes:
    logger.info(f"Downloading PDF from GCS bucket: {bucket_name}")
    bucket = _client.bucket(bucket_name)
    blob = bucket.blob(object_name)
    return blob.download_as_bytes()


def get_metadata(bucket_name: str, object_name: str) -> Dict[str, str]:
    logger.info(f"Fetching metadata from GCS object: gs://{bucket_name}/{object_name}")
    bucket = _client.bucket(bucket_name)
    blob = bucket.blob(object_name)
    blob.reload()
    return blob.metadata or {}


def update_metadata(
    bucket_name: str,
    object_name: str,
    updates: Dict[str, str],
):
    logger.info(f"Updating metadata for GCS object: gs://{bucket_name}/{object_name}")
    bucket = _client.bucket(bucket_name)
    blob = bucket.blob(object_name)

    blob.reload()
    current = blob.metadata or {}
    current.update(updates)

    blob.metadata = current
    blob.patch()