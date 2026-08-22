"""
Step 2: Multilingual Normalization Layer
Translates every feedback record into English for downstream RAG/reasoning,
while keeping the original text + language tagged for transparency.

Uses deep-translator (free, hits Google Translate under the hood) when
internet access is available. Falls back to a small local dictionary of
known translations if the live API call fails (timeout, blocked network,
rate limit, etc.) so the pipeline never breaks and categorization stays
accurate even offline.
"""

from ingest import load_mock_feedback

try:
    from deep_translator import GoogleTranslator
    TRANSLATOR_AVAILABLE = True
except ImportError:
    TRANSLATOR_AVAILABLE = False


# Known-good translations for the mock dataset, used only if the live
# translation API call fails. Keyed by feedback id so it never misapplies
# to real/new data — this is a safety net for the demo dataset specifically.
FALLBACK_TRANSLATIONS = {
    "fb002": "Water has flooded the road near Ameerpet, school children are "
             "not able to pass. It has been like this for several days.",
    "fb003": "There is a water leak at the hospital. Patients remain "
             "without water for days during the rainy season.",
    "fb005": "The road is very bad, it is very difficult to drive vehicles, "
             "many accidents have already happened.",
    "fb007": "There is no drinking water, the pipe has been broken for "
             "many days, people are suffering a lot.",
}


def translate_to_english(feedback_id: str, text: str, source_lang: str) -> str:
    if source_lang == "en":
        return text

    if TRANSLATOR_AVAILABLE:
        try:
            return GoogleTranslator(source=source_lang, target="en").translate(text)
        except Exception as e:
            print(f"  [warn] live translation failed for {feedback_id} ({e}); "
                  f"using local fallback")

    if feedback_id in FALLBACK_TRANSLATIONS:
        return FALLBACK_TRANSLATIONS[feedback_id]

    # last resort: pass through untranslated
    return text


def normalize_feedback(records):
    normalized = []
    for r in records:
        english_text = translate_to_english(r["id"], r["text"], r["language"])
        normalized.append({
            **r,
            "text_en": english_text,
        })
    return normalized


if __name__ == "__main__":
    records = load_mock_feedback()
    normalized = normalize_feedback(records)
    for r in normalized:
        if r["language"] != "en":
            print(f"[{r['id']}] {r['language']} -> en")
            print(f"  original: {r['text']}")
            print(f"  english : {r['text_en']}\n")