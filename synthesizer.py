from openai import OpenAI

def build_context(scraped_articles: list) -> str:
    context = ""

    for i, article in enumerate(scraped_articles):
        context += f"""
--- Source {i+1}: {article['title']} ---
URL: {article['url']}
{article['content']}
"""

    return context.strip()


def synthesizer_agent(topic: str, scraped_articles: list) -> str:
    print("[Synthesizer Agent] Synthesizing findings...")

    if not scraped_articles:
        print("[Synthesizer Agent] No articles to synthesize.")
        return "No content was retrieved to synthesize."

    context = build_context(scraped_articles)

    system_prompt = """
You are an expert research synthesizer.
You will be given content from multiple sources on a topic.
Your job is to:
- Merge all the information into one clean, unified summary
- Remove any repetition across sources
- Highlight the most important findings
- Note any contradictions between sources
- Keep it factual, clear and well structured
- Use plain paragraphs, no bullet points
Do NOT make up any information. Only use what is provided.
"""

    user_prompt = f"""
                   Topic: {topic}
                   Here is the content retrieved from multiple sources:
                   {context}
                   Now synthesize all of this into a clean, unified research summary.
                """
    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key="openrouter-api-key",  # add openrouter api key
    )
    response_text = ""

    if context:

        response_text = ""

        completion = client.chat.completions.create(
            extra_body={},
            model="nvidia/nemotron-3-super-120b-a12b:free",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            stream=True
        )

        for chunk in completion:
            if chunk.choices[0].delta.content:
                response_text += chunk.choices[0].delta.content


    print(f"[Synthesizer Agent] Synthesis complete — {len(response_text)} chars.")
    return response_text
