"""Parse the public BCA-NY member directory into evidence-backed contacts."""
from __future__ import annotations
import re
import httpx
from bs4 import BeautifulSoup
from .normalize import normalize_email, normalize_phone

URL = "https://www.ny-bca.com/member-directory/"
TITLE_RE = re.compile(r"^(Owner|President|CEO|Vice President|VP|Director|Project Manager|Preconstruction Manager|Estimator|BIM Manager|Principal|Partner|Officer|Executive VP|Dir\. of Oper\.|Dir\. of Construction|Owner/Pres\.)", re.I)
EMAIL_RE = re.compile(r"[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}", re.I)
PHONE_RE = re.compile(r"(?:\+?1[\s.-]?)?(?:\(?\d{3}\)?[\s.-]?)\d{3}[\s.-]\d{4}")


def fetch_directory(url: str = URL) -> str:
    r = httpx.get(url, timeout=30, follow_redirects=True, headers={"User-Agent": "construction-lead-engine/0.1"})
    r.raise_for_status()
    return r.text


def parse_directory(html: str, url: str = URL) -> list[dict]:
    soup = BeautifulSoup(html, "html.parser")
    text = soup.get_text("\n", strip=True)
    lines = [re.sub(r"\s+", " ", x).strip() for x in text.splitlines() if x.strip()]
    leads: list[dict] = []
    company = ""
    person = ""
    title = ""
    for line in lines:
        if line.startswith("Image:"):
            continue
        mtitle = TITLE_RE.match(line)
        if mtitle:
            title = line
            continue
        if "Image:" in line:
            continue
        if EMAIL_RE.fullmatch(line) or PHONE_RE.fullmatch(line):
            continue
        # A directory entry is usually followed by address, then named people/titles.
        # Keep parsing conservative: only emit a record once a public email or phone appears.
        if company and person and title:
            emails = EMAIL_RE.findall(line)
            phones = PHONE_RE.findall(line)
            if emails or phones:
                leads.append({"company": company, "decision_maker": person, "title": title,
                              "work_email": normalize_email(emails[0]) if emails else "",
                              "direct_business_phone": normalize_phone(phones[0]) if phones else "",
                              "email_status": "public" if emails else "unverified",
                              "phone_status": "public" if phones else "unverified",
                              "evidence_urls": url})
                person = title = ""
                continue
        # Avoid treating addresses and labels as people; names in the directory are generally short.
        if company == "" and len(line) < 100 and not any(ch.isdigit() for ch in line):
            company = line
        elif company and not person and len(line) < 70 and not any(ch.isdigit() for ch in line):
            person = line
    return leads
