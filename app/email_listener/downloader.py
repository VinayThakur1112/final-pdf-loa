import os

DOWNLOAD_DIR = "incoming"

os.makedirs(DOWNLOAD_DIR, exist_ok=True)

def download_pdf(part, tid):
    filename = part.filename

    if not filename.lower().endswith(".pdf"):
        return None

    # if not filename.lower().startswith("output"):
    #     return None

    file_path = os.path.join(DOWNLOAD_DIR, tid + "_" + filename)

    with open(file_path, "wb") as f:
        f.write(part.get_payload())

    return file_path