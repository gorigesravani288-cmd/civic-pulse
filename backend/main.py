"""
Step 5: Backend API
Serves the RAG search + prioritized hotspots to the frontend dashboard.

Run locally with:
    uvicorn backend.main:app --reload --port 8000

To connect real Supabase storage instead of in-memory data:
    pip install supabase
    from supabase import create_client
    supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
    # replace build_index()/build_hotspots() calls with supabase.table(...).select()
"""

import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), "..", "src"))

from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional

from rag_core import build_index
from prioritize import build_hotspots, llm_summary_prompt, generate_llm_summary

app = FastAPI(title="AI for Digital Public Infrastructure & Governance API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Build once at startup (swap for DB-backed lookups in production)
_index = build_index()
_hotspots = build_hotspots()


@app.get("/")
def root():
    return {"status": "ok", "service": "gov-ai-infrastructure-backend"}


@app.get("/feedback/search")
def search_feedback(q: str = Query(..., description="Search query"),
                     region: Optional[str] = None,
                     top_k: int = 5):
    results = _index.retrieve(q, top_k=top_k, region=region)
    return [
        {
            "id": r["id"],
            "region": r["region"],
            "language": r["language"],
            "channel": r["channel"],
            "text_en": r["text_en"],
            "relevance_score": round(float(score), 3),
        }
        for r, score in results
    ]


@app.get("/hotspots")
def get_hotspots():
    return _hotspots


@app.get("/hotspots/{index}/summary_prompt")
def get_summary_prompt(index: int):
    """Returns the prompt you'd send to an LLM for a policymaker-ready brief."""
    if index < 0 or index >= len(_hotspots):
        return {"error": "hotspot index out of range"}
    return {"prompt": llm_summary_prompt(_hotspots[index])}


@app.get("/hotspots/{index}/summary")
def get_ai_summary(index: int):
    """Returns a real Gemini-generated policymaker briefing for a hotspot."""
    if index < 0 or index >= len(_hotspots):
        return {"error": "hotspot index out of range"}
    result = generate_llm_summary(_hotspots[index])
    return {
        "region": _hotspots[index]["region"],
        "category": _hotspots[index]["category"],
        **result,
    }