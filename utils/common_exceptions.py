"""
common_exceptions.py
---------------------
Custom exceptions used across the FundWise project.
"""


class FundWiseError(Exception):
    """Base exception for FundWise"""
    pass


class ValidationError(FundWiseError):
    """Raised when input validation fails"""
    pass


class ConfigError(FundWiseError):
    """Raised when configuration loading fails"""
    pass


class DatabaseError(FundWiseError):
    """Raised when DB connection or query fails"""
    pass
