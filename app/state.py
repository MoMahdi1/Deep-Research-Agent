from typing import TypedDict, List, Optional

class ResearchState(TypedDict):
    question: str
    rewritten_query: Optional[str]
    search_queries: List[str]
    web_results: List[str]
    doc_results: List[str]
    critique: Optional[str]
    final_report: Optional[str]
    current_step: str