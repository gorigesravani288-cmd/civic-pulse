"""
Step 3: RAG Core
Embeds normalized feedback and enables semantic retrieval:
  "what are the top infrastructure complaints in region X?"

This version uses TF-IDF + cosine similarity (scikit-learn) so it runs fully
offline with zero API keys — good for a hackathon demo.

To upgrade to real semantic embeddings later (recommended for production):
  from sentence_transformers import SentenceTransformer
  model = SentenceTransformer("all-MiniLM-L6-v2")
  vectors = model.encode(texts)
  # store vectors in Chroma/Qdrant instead of the TfidfVectorizer below

Swapping the embedding step is the only change needed — the retrieval
interface (`retrieve`) stays the same.
"""

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from ingest import load_mock_feedback
from translate_layer import normalize_feedback


class FeedbackIndex:
    def __init__(self, records):
        self.records = records
        self.texts = [r["text_en"] for r in records]
        self.vectorizer = TfidfVectorizer(stop_words="english")
        self.matrix = self.vectorizer.fit_transform(self.texts)

    def retrieve(self, query: str, top_k: int = 5, region: str = None):
        """Return the top_k most relevant feedback records for a query,
        optionally filtered to a specific region."""
        query_vec = self.vectorizer.transform([query])
        scores = cosine_similarity(query_vec, self.matrix).flatten()

        ranked = sorted(
            zip(self.records, scores), key=lambda x: x[1], reverse=True
        )
        if region:
            ranked = [(r, s) for r, s in ranked if region.lower() in r["region"].lower()]

        return ranked[:top_k]


def build_index():
    records = load_mock_feedback()
    normalized = normalize_feedback(records)
    return FeedbackIndex(normalized)


if __name__ == "__main__":
    index = build_index()

    query = "water supply problems"
    results = index.retrieve(query, top_k=3)

    print(f"Query: '{query}'\n")
    for record, score in results:
        print(f"  score={score:.3f} [{record['region']}] {record['text_en'][:90]}")
