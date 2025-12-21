import pdfplumber
import logging
import json

logger = logging.getLogger(__name__)

class PDFParser:
    def parse_pdf(self, file_path):
        """
        Parses a PDF file and extracts text and tables.
        Returns a dictionary with 'text' and 'tables' (list of JSONs).
        """
        result = {
            'text': "",
            'tables': []
        }
        
        try:
            with pdfplumber.open(file_path) as pdf:
                for page in pdf.pages:
                    # Extract Text
                    text = page.extract_text()
                    if text:
                        result['text'] += text + "\n"
                    
                    # Extract Tables
                    # extract_table returns a list of lists (rows)
                    tables = page.extract_tables()
                    for table in tables:
                        # Convert list of lists to a more structured format if needed
                        # For now, just keeping it as a list of rows
                        if table:
                           result['tables'].append(table)
            
            logger.info(f"Successfully parsed {file_path}. Extracted {len(result['tables'])} tables.")
            return result
            
        except Exception as e:
            logger.error(f"Error parsing PDF {file_path}: {e}")
            return None
