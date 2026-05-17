from app.agents.retriever_agent import retriever_agent


query = "ما الفرق بين البطلان المطلق والبطلان النسبي؟"

result = retriever_agent(query)

print("\n========== FINAL RESULT ==========\n")

print(f"Source: {result['source']}")
print(f"Fallback Used: {result['fallback_used']}")

print("\nResults:\n")

for i, r in enumerate(result["results"]):

    print(f"\n--- Result {i+1} ---\n")

    if isinstance(r, dict):

        print(r.get("content", ""))

        if "url" in r:
            print(f"\nURL: {r['url']}")

        if "score" in r:
            print(f"Score: {r['score']}")

    else:
        print(r)