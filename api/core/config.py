"""
config.py
---------
Loads configurations from environment + .ini
"""

import os
import configparser

class AppConfig:
    def __init__(self):
        config = configparser.ConfigParser()
        config.read("deployment_config/main_config.ini")

        self.db_url = os.getenv("DATABASE_URL")
        self.secret_key = os.getenv("FASTAPI_SECRET_KEY")
        self.upi_key = os.getenv("UPI_API_KEY")

config = AppConfig()
