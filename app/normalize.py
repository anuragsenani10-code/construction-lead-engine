"""Normalize extracted public contacts without guessing missing information."""
from __future__ import annotations
import re


def normalize_phone(value: str) -> str:
    digits = re.sub(r"\D", "", value or "")
    if len(digits) == 11 and digits.startswith("1"):
        digits = digits[1:]
    if len(digits) == 10:
        return f"+1 ({digits[:3]}) {digits[3:6]}-{digits[6:]}"
    return value.strip()


def normalize_email(value: str) -> str:
    return value.strip().lower()


def public_contact_status(value: str, source_url: str) -> str:
    return "public" if value and source_url else "unverified"
