from tavily import TavilyClient

tavily_api_key = TavilyClient(api_key="tavily-api-key") # Add tavily api key

def search_agent(topic) -> dict:
    print("[Search Agent] Searching for sources...")

    response = tavily_api_key.search(
        query=topic,
        search_depth="advanced",
        max_results=10,
        include_answer=False,
        include_raw_content=False,
    )

    results = []
    for r in response.get("results", []):
        results.append({
            "title": r.get("title", ""),
            "url": r.get("url", ""),
            "snippet": r.get("content", ""),
            "score": r.get("score", 0.0),
        })

    print(f"[Search Agent] Found {len(results)} results.")
    return results
