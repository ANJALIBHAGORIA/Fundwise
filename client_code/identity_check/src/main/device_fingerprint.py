"""
device_fingerprint.py
---------------------
Purpose:
    Generate unique device fingerprints to detect duplicate or suspicious accounts.
    Compare fingerprints with existing database of devices.
"""

import hashlib
from typing import Dict, List

class DeviceFingerprint:
    def __init__(self, existing_fingerprints: List[str] = None):
        """
        Args:
            existing_fingerprints: Optional list of known fingerprints to check for duplicates
        """
        self.existing_fingerprints = existing_fingerprints or []

    def generate_fingerprint(self, device_info: Dict[str, str]) -> str:
        """
        Generate SHA256 hash fingerprint for device
        Args:
            device_info: Dictionary with keys: ip, user_agent, os, browser
        Returns:
            str: fingerprint hash
        """
        fingerprint_str = f"{device_info.get('ip')}|{device_info.get('user_agent')}|{device_info.get('os')}|{device_info.get('browser')}"
        return hashlib.sha256(fingerprint_str.encode()).hexdigest()

    def is_duplicate(self, fingerprint: str) -> bool:
        """
        Check if fingerprint already exists
        Args:
            fingerprint: device hash
        Returns:
            bool: True if duplicate, False otherwise
        """
        return fingerprint in self.existing_fingerprints

    def add_fingerprint(self, fingerprint: str):
        """
        Add new fingerprint to the database/list
        """
        if fingerprint not in self.existing_fingerprints:
            self.existing_fingerprints.append(fingerprint)


if __name__ == "__main__":
    device_info = {
        "ip": "192.168.1.10",
        "user_agent": "Mozilla/5.0",
        "os": "Windows 11",
        "browser": "Chrome"
    }
    fingerprint_engine = DeviceFingerprint()
    fp = fingerprint_engine.generate_fingerprint(device_info)
    print("Fingerprint:", fp)
    print("Is duplicate?", fingerprint_engine.is_duplicate(fp))
