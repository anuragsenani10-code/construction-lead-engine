"""Small Crawl4AI adapter; imports lazily so the CLI remains testable without a browser."""
from __future__ import annotations

async def crawl_urls(urls: list[str]) -> list[dict]:
    try:
        from crawl4ai import AsyncWebCrawler
    except ImportError as exc:
        raise RuntimeError("Install requirements and run Crawl4AI browser setup before crawling.") from exc

    results = []
    async with AsyncWebCrawler() as crawler:
        for url in urls:
            try:
                result = await crawler.arun(url=url)
                results.append({"url": url, "html": getattr(result, "html", "") or "", "markdown": getattr(result, "markdown", "") or ""})
            except Exception as exc:
                results.append({"url": url, "html": "", "markdown": "", "error": str(exc)})
    return results
