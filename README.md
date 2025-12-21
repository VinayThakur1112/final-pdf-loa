# PDF Data Extraction Pipeline

A Python-based pipeline that reads emails from a GCP-integrated source, downloads PDF attachments, extracts tabular data, and stores it in a SQL database.

## Architecture
- **Email Source**: Gmail API
- **Processing**: Python (pdfplumber)
- **Database**: SQLite (Dev) / PostgreSQL (Prod)
- **Deployment**: Docker + Kubernetes

## Setup

1.  **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

2.  **Environment Variables**:
    Create a `.env` file with:
    ```
    DATABASE_URL=sqlite:///data.db
    # GCP Credentials should be mounted or referenced via GOOGLE_APPLICATION_CREDENTIALS
    ```

3.  **Run**:
    ```bash
    python -m src.main
    ```
