BLOCKED_DOMAINS = [
    "reddit.com", "quora.com", "pinterest.com",
    "facebook.com", "twitter.com", "instagram.com",
    "tiktok.com", "youtube.com", "slideshare.net",
    "scribd.com", "chegg.com",
]

TRUSTED_DOMAINS = [
    "wikipedia.org", "britannica.com", "nature.com",
    "sciencedirect.com", "ieee.org", "arxiv.org",
    "ibm.com", "google.com", "microsoft.com", "mit.edu",
    "stanford.edu", "bbc.com", "reuters.com", "forbes.com",
    "techcrunch.com", "wired.com", "medium.com",
]

MIN_SCORE = 0.5
MAX_RESULTS = 5

def is_blocked(url: str) -> bool:
    for domain in BLOCKED_DOMAINS:
        if domain in url:
            return True
    return False

def is_trusted(url: str) -> bool:
    for domain in TRUSTED_DOMAINS:
        if domain in url:
            return True
    return False

def verifier_agent(results: list) -> list:
    print("[Verifier Agent] Verifying sources...")

    verified = []

    for r in results:
        url = r.get("url", "")
        score = r.get("score", 0.0)

        if is_blocked(url):
            print(f"  [BLOCKED]  {url}")
            continue

        if score < MIN_SCORE:
            print(f"  [LOW SCORE] {url} — score: {score}")
            continue

        r["trusted"] = is_trusted(url)

        print(f"  [PASSED] {url} — score: {score} — trusted: {r['trusted']}")
        verified.append(r)

    verified.sort(key=lambda x: (x["trusted"], x["score"]), reverse=True)

    verified = verified[:MAX_RESULTS]

    print(f"[Verifier Agent] {len(verified)} sources passed verification.")
    return verified
