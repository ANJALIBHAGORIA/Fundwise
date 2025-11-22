"""
document_verifier.py
--------------------
Purpose:
    Perform Optical Character Recognition (OCR) on user documents, validate text content
    using rule-based checks, and flag suspicious documents for further review.

Dependencies:
    - pytesseract: OCR engine
    - PIL: Image handling
    - re: regex for pattern matching
    - yaml: to load fraud detection rules
"""

import pytesseract
from PIL import Image
import re
import yaml
from typing import Dict, List


class DocumentVerifier:
    def __init__(self, rules_file: str = "fraud_document_rules.yaml"):
        """
        Initialize DocumentVerifier with rules.
        Args:
            rules_file: YAML file containing regex rules for fraud detection
        """
        with open(rules_file) as f:
            self.rules = yaml.safe_load(f)

    def ocr_extract_text(self, image_path: str) -> str:
        """
        Extract text from a document image using OCR
        Args:
            image_path: Path to the document image
        Returns:
            str: extracted text
        """
        image = Image.open(image_path)
        text = pytesseract.image_to_string(image)
        return text

    def validate_text(self, text: str) -> Dict[str, List[str]]:
        """
        Apply rule-based checks to OCR text
        Args:
            text: OCR extracted text
        Returns:
            dict: {'status': 'verified'/'suspicious', 'issues': [list of matched rules]}
        """
        issues = []
        for rule_name, pattern in self.rules.get("patterns", {}).items():
            if re.search(pattern, text, re.IGNORECASE):
                issues.append(rule_name)
        status = "suspicious" if issues else "verified"
        return {"status": status, "issues": issues}

    def verify_document(self, image_path: str) -> Dict[str, List[str]]:
        """
        Complete document verification pipeline
        Args:
            image_path: path to uploaded document image
        Returns:
            dict: verification result
        """
        text = self.ocr_extract_text(image_path)
        result = self.validate_text(text)
        return result


if __name__ == "__main__":
    verifier = DocumentVerifier()
    result = verifier.verify_document("sample_id.png")
    print(result)
