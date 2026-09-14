"""Conservative extraction of publicly published professional contacts."""
from __future__ import annotations
import re
from bs4 import BeautifulSoup

EMAIL_RE = re.compile(r"[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}", re.I)
PHONE_RE = re.compile(r"(?:\+?1[\s.-]?)?(?:\(?\d{3}\)?[\s.-]?)\d{3}[\s.-]\d{4}")
TITLE_RE = re.compile(r"\b(Owner|President|CEO|Vice President|VP|Director|Project Manager|Preconstruction Manager|Estimator|BIM Manager)\b", re.I)


def extract_public_contacts(html: str, url: str = "") -> list[dict]:
    soup = BeautifulSoup(html, "html.parser")
    contacts = []
    seen = set()
    for node in soup.select("a[href^='mailto:'], a[href^='tel:']"):
        href = node.get("href", "")
        value = href.split(":", 1)[1].split("?", 1)[0].strip()
        if not value:
            continue
        kind = "email" if href.lower().startswith("mailto:") else "phone"
        key = (kind, value.lower())
        if key in seen:
            continue
        seen.add(key)
        parent = node.parent.get_text(" ", strip=True) if node.parent else ""
        contacts.append({"type": kind, "value": value, "context": parent[:500], "source_url": url, "public": True})

    text = soup.get_text(" ", strip=True)
    for value in EMAIL_RE.findall(text):
        key = ("email", value.lower())
        if key not in seen:
            seen.add(key)
            contacts.append({"type": "email", "value": value, "context": text[:500], "source_url": url, "public": True})
    return contacts


def extract_titles(text: str) -> list[str]:
    return sorted({m.group(0) for m in TITLE_RE.finditer(text)}, key=str.lower)
