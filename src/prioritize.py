"""
Step 4: Reasoning / Prioritization Layer
Clusters feedback by region + category, scores urgency, and produces a
ranked list of "demand hotspots" for policymakers.

Urgency scoring here is rule-based (keyword severity + volume) so it runs
with zero API cost. The generate_llm_summary() function below calls Gemini
to turn a hotspot into a real policymaker-ready briefing.
"""

import os
from pathlib import Path
from collections import defaultdict

from dotenv import load_dotenv

from rag_core import build_index

# Load .env from the project root regardless of where this script runs from
load_dotenv(dotenv_path=Path(__file__).resolve().parent / ".env")

try:
    from google import genai
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    if GEMINI_API_KEY:
        _client = genai.Client(api_key=GEMINI_API_KEY)
        GEMINI_AVAILABLE = True
    else:
        GEMINI_AVAILABLE = False
except ImportError:
    GEMINI_AVAILABLE = False


SEVERITY_KEYWORDS = {
    "accident": 3, "flood": 3, "hospital": 3, "no water": 3, "health hazard": 2,
    "unsafe": 2, "days": 1, "week": 1, "month": 1, "broken": 2, "not worked": 2,
}

CATEGORY_KEYWORDS = {
    "Water & Sanitation": ["water", "pipeline", "drinking"],
    "Roads & Transport": ["road", "pothole", "accident", "traffic"],
    "Health Infrastructure": ["hospital", "patients", "clinic"],
    "Public Safety": ["street light", "unsafe", "school"],
    "Waste Management": ["garbage", "collection", "hazard"],
}


def categorize(text: str) -> str:
    text_lower = text.lower()
    for category, keywords in CATEGORY_KEYWORDS.items():
        if any(kw in text_lower for kw in keywords):
            return category
    return "Uncategorized"


def score_urgency(text: str) -> int:
    text_lower = text.lower()
    return sum(weight for kw, weight in SEVERITY_KEYWORDS.items() if kw in text_lower)


def build_hotspots():
    index = build_index()
    clusters = defaultdict(list)

    for record in index.records:
        category = categorize(record["text_en"])
        key = (record["region"], category)
        clusters[key].append(record)

    hotspots = []
    for (region, category), records in clusters.items():
        urgency = sum(score_urgency(r["text_en"]) for r in records)
        hotspots.append({
            "region": region,
            "category": category,
            "num_reports": len(records),
            "urgency_score": urgency,
            "sample_feedback": records[0]["text_en"],
        })

    hotspots.sort(key=lambda h: h["urgency_score"], reverse=True)
    return hotspots


def llm_summary_prompt(hotspot: dict) -> str:
    """
    Prompt sent to Gemini to generate a policymaker-ready summary.
    """
    return (
        f"You are briefing a government policymaker. There are "
        f"{hotspot['num_reports']} citizen reports in {hotspot['region']} "
        f"about '{hotspot['category']}'. Sample report: \"{hotspot['sample_feedback']}\". "
        f"Write a 2-sentence executive summary and recommend one concrete action."
    )


def generate_llm_summary(hotspot: dict) -> dict:
    """
    Calls Gemini to generate a real policymaker-ready briefing for a hotspot.
    Falls back to a clear message if no API key is configured or the call fails.
    """
    if not GEMINI_AVAILABLE:
        return {
            "summary": "LLM not configured. Add GEMINI_API_KEY to your .env file to enable AI-generated briefings.",
            "source": "fallback",
        }

    prompt = llm_summary_prompt(hotspot)

    try:
        response = _client.models.generate_content(
            model="gemini-3.6-flash",
            contents=prompt,
        )
        return {
            "summary": response.text.strip(),
            "source": "gemini-2.0-flash",
        }
    except Exception as e:
        return {
            "summary": f"Could not generate summary right now ({e}).",
            "source": "error",
        }


if __name__ == "__main__":
    hotspots = build_hotspots()
    print("Top demand hotspots (ranked by urgency):\n")
    for h in hotspots:
        print(f"[{h['urgency_score']} pts] {h['region']} — {h['category']} "
              f"({h['num_reports']} reports)")
        print(f"   e.g. \"{h['sample_feedback']}\"\n")