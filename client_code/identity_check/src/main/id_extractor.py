"""
id_extractor.py
----------------
Purpose:
    Extract structured fields (Name, DOB, ID number, Address) from OCR text
    for digital identity verification.
"""

import re
from typing import Dict

class IDExtractor:
    def __init__(self):
        """
        Initialize extractor with regex patterns.
        """
        self.patterns = {
            "name": r"Name[:\-]?\s*([A-Za-z\s]+)",
            "dob": r"DOB[:\-]?\s*(\d{2}/\d{2}/\d{4})",
            "id_number": r"ID[:\-]?\s*([A-Z0-9]+)",
            "address": r"Address[:\-]?\s*(.*)"  
        }

    def extract_fields(self, text: str) -> Dict[str, str]:
        """
        Extract fields based on patterns
        Args:
            text: OCR extracted text
        Returns:
            dict: Extracted fields
        """
        extracted = {}
        for field, pattern in self.patterns.items():
            match = re.search(pattern, text, re.IGNORECASE)
            extracted[field] = match.group(1).strip() if match else None
        return extracted


if __name__ == "__main__":
    sample_text = """
    Name: John Doe
    DOB: 01/01/1990
    ID: ABC123456
    Address: 123, MG Road, Bangalore
    """
    extractor = IDExtractor()
    fields = extractor.extract_fields(sample_text)
    print(fields)
