from typing import Dict, Any, List

from app.tools.retriever import vectorstore
from app.tools.search import web_search


MIN_RELEVANT_DOCS = 2
MAX_SCORE_THRESHOLD = 0.30


def retriever_agent(query: str) -> Dict[str, Any]:
    """
    Corrective RAG Agent

    Flow:
    1. Search local ChromaDB
    2. Evaluate retrieval quality
    3. If weak retrieval -> web fallback
    """

    try:
        print(f"[retrieval_agent] Searching docs for: {query}")

        docs_with_scores = vectorstore.similarity_search_with_score(
            query=query,
            k=5
        )

        filtered_docs: List[Dict[str, Any]] = []

        for doc, score in docs_with_scores:

            print(f"[retriever_agent] Score: {score}")

            if score > MAX_SCORE_THRESHOLD:
                continue

            filtered_docs.append({
                "content": doc.page_content,
                "metadata": doc.metadata,
                "score": float(score)
            })

        
        # Good retrieval → use docs
        
        if len(filtered_docs) >= MIN_RELEVANT_DOCS:

            print(
                f"[retriever_agent] Found {len(filtered_docs)} relevant docs in ChromaDB"
            )

            return {
                "source": "documents",
                "results": filtered_docs,
                "fallback_used": False,
            }

       
        # Fallback → Web search
        
        print(
            "[retriever_agent] Local retrieval insufficient --> falling back to web"
        )

        web_results = web_search(query)

        return {
            "source": "web",
            "results": filtered_docs + web_results,
            "fallback_used": True,
        }

    except Exception as e:

        print(f"[retriever_agent] Error: {str(e)}")

        return {
            "source": "error",
            "results": [],
            "fallback_used": False,
            "error": str(e)
        }