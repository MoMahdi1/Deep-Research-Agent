from retriever import vectorstore

query = "ما الفرق بين البطلان المطلق والبطلان النسبي؟"

docs = vectorstore.similarity_search_with_score(
    query=query,
    k=3
)

for i, (doc, score) in enumerate(docs):

    print(f"\n--- Result {i+1} ---")
    print(f"Score: {score}\n")

    print(doc.page_content)