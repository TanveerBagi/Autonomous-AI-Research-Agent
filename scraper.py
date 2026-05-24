import requests

JINA_BASE_URL = "https://r.jina.ai/"
MAX_CHARS = 1500

def scrape_url(url: str) -> str:
    try:
        response = requests.get(
            JINA_BASE_URL + url,
            timeout=10,
            headers={"Accept": "text/plain"}
        )

        if response.status_code == 200:
            content = response.text.strip()
            return content[:MAX_CHARS]
        else:
            print(f"  [FAILED] {url} — status: {response.status_code}")
            return ""

    except requests.exceptions.Timeout:
        print(f"  [TIMEOUT] {url}")
        return ""

    except requests.exceptions.RequestException as e:
        print(f"  [ERROR] {url} — {e}")
        return ""


def scraper_agent(verified_results: list) -> list:
    print("[Scraper Agent] Scraping verified sources...")

    scraped = []

    for r in verified_results:
        url = r.get("url", "")
        print(f"  [Scraping] {url}")

        content = scrape_url(url)

        if content:
            scraped.append({
                "title": r.get("title", ""),
                "url": url,
                "snippet": r.get("snippet", ""),
                "trusted": r.get("trusted", False),
                "content": content,
            })
            print(f"  [Done] {len(content)} chars extracted")
        else:
            print(f"  [Skipped] No content retrieved")

    print(f"[Scraper Agent] {len(scraped)} articles successfully scraped.")
    return scraped
