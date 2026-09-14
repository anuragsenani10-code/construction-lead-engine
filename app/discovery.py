"""Low-cost web discovery adapters for construction leads."""
from __future__ import annotations
import os
from urllib.parse import quote
import httpx


def brave_search(query: str, count: int = 20) -> list[dict]:
    """Search Brave when SEARCH_API_KEY is configured; return evidence URLs only."""
    key = os.getenv("SEARCH_API_KEY", "").strip()
    if not key:
        return []
    url = "https://api.search.brave.com/res/v1/web/search"
    headers = {"Accept": "application/json", "X-Subscription-Token": key}
    params = {"q": query, "count": count}
    r = httpx.get(url, headers=headers, params=params, timeout=20)
    r.raise_for_status()
    data = r.json()
    return [
        {"title": x.get("title", ""), "url": x.get("url", ""), "description": x.get("description", "")}
        for x in data.get("web", {}).get("results", [])
        if x.get("url")
    ]


def build_queries(location: str, industries: list[str]) -> list[str]:
    terms = ["construction", "contractor", "general contractor", "construction management", "BIM", "MEP"]
    return [f'"{location}" "{term}" (hiring OR projects OR BIM OR preconstruction)' for term in terms]
