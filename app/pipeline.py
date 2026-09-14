"""Pipeline for discovering, crawling, extracting and scoring evidence-backed leads."""
from __future__ import annotations
import asyncio
from .config import Settings
from .discovery import brave_search, build_queries
from .crawler import crawl_urls
from .extraction import extract_public_contacts, extract_titles
from .models import Lead
from .scoring import detect_pain_signals, score_lead, priority


def _candidate_urls(settings: Settings) -> list[str]:
    urls: list[str] = []
    for q in build_queries(settings.location, settings.industries):
        for result in brave_search(q, count=min(10, settings.lead_limit)):
            url = result.get("url", "")
            if url and url not in urls:
                urls.append(url)
    return urls[: settings.lead_limit * 3]


def _lead_from_page(page: dict, settings: Settings) -> list[Lead]:
    html = page.get("html", "")
    if not html:
        return []
    url = page.get("url", "")
    contacts = extract_public_contacts(html, url)
    text = page.get("markdown", "") or html
    titles = extract_titles(text)
    signals = detect_pain_signals(text)
    emails = [c["value"] for c in contacts if c["type"] == "email"]
    phones = [c["value"] for c in contacts if c["type"] == "phone"]
    if not emails and not phones:
        return []
    company = page.get("title", "") or url.split("/")[2] if "/" in url else url
    title = titles[0] if titles else ""
    email = emails[0] if emails else ""
    phone = phones[0] if phones else ""
    score = score_lead(signals, bool(email), bool(phone))
    return [Lead(company=company, website=url, location=settings.location,
                 industry="Construction", decision_maker="", title=title,
                 work_email=email, direct_business_phone=phone,
                 email_status="public" if email else "unverified",
                 phone_status="public" if phone else "unverified",
                 pain_signals=", ".join(signals), evidence_urls=url,
                 score=score, priority=priority(score),
                 reason="Public contact evidence plus detected site signals.")]


def run(settings: Settings) -> list[Lead]:
    urls = _candidate_urls(settings)
    pages = asyncio.run(crawl_urls(urls)) if urls else []
    leads: list[Lead] = []
    seen = set()
    for page in pages:
        for lead in _lead_from_page(page, settings):
            key = (lead.website, lead.work_email, lead.direct_business_phone)
            if key not in seen:
                seen.add(key)
                leads.append(lead)
            if len(leads) >= settings.lead_limit:
                return leads
    return leads
