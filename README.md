# Civic Pulse

**AI for Digital Public Infrastructure & Governance**
Built for *Build with AI: Code for Communities — Second Edition* (Google Cloud × Hack2Skill)

Civic Pulse turns scattered citizen infrastructure complaints — voice, text, and messaging, in any language — into a single ranked register a policymaker can act on in minutes, not weeks.

---

## The problem

Citizen feedback about infrastructure arrives fragmented: voice calls, WhatsApp, IVR, and web forms, in a dozen languages, with no shared system to read them together. Officials have no way to tell that ten flooding reports in one ward matter more than a single pothole complaint elsewhere. By the time a real risk — a hospital losing water supply — surfaces through normal channels, it's already a crisis, not an early warning.

## What Civic Pulse does

A Digital Public Good that:
1. **Ingests** citizen reports across languages and channels
2. **Normalizes** them into a common working language
3. **Retrieves** relevant reports through a RAG search layer
4. **Prioritizes** by clustering region + issue and scoring urgency
5. **Briefs** — Gemini drafts a policymaker-ready executive summary on demand
6. **Acts** — the ranked register goes live on a public-facing dashboard

Every step above is implemented and tested — not a mockup.

---

## Live demo

- **Dashboard:** `dashboard/index.html` — two themes (Gazette / Night Watch), a live urgency pulse strip, RAG-powered search, and one-click AI briefings
- **Demo script:** see [`DEMO_SCRIPT.md`](./DEMO_SCRIPT.md) for the full pitch + live-demo walkthrough
- **Pitch deck:** [`civic_pulse_pitch_deck.pptx`](./civic_pulse_pitch_deck.pptx)

---

## Architecture
mock_feedback.json (voice / text / messaging, multi-language)
│
▼
src/ingest.py → load raw feedback + Whisper transcription
│
▼
src/translate_layer.py → normalize to English (deep-translator, safe fallback)
│
▼
src/rag_core.py → TF-IDF embed + cosine-similarity retrieval
│
▼
src/prioritize.py → cluster by region/category, score urgency, Gemini briefings
│
▼
backend/main.py → FastAPI: /hotspots, /feedback/search, /hotspots/{i}/summary
│
▼
dashboard/index.html → live register, pulse strip, search, AI briefings

---

## Tech stack

| Layer | Tool |
|---|---|
| Reasoning & briefings | Google Gemini (`gemini-3.6-flash`) |
| Voice transcription | OpenAI Whisper |
| Retrieval | Custom RAG (TF-IDF + cosine similarity) |
| Translation | deep-translator, with safe local fallback |
| Backend | FastAPI |
| Frontend | Vanilla HTML/CSS/JS — no build step |
| Storage | In-memory (Supabase-ready) |

---

## Running it locally

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Add your Gemini API key
echo "GEMINI_API_KEY=your_key_here" > src/.env

# 3. Start the backend
python -m uvicorn backend.main:app --reload --port 8000

# 4. In a second terminal, serve the dashboard
cd dashboard
python -m http.server 5600

# 5. Open the dashboard
# http://127.0.0.1:5600
```

API docs (Swagger) are available at `http://127.0.0.1:8000/docs`.

---

## What's tested and working

- ✅ Multilingual ingestion of voice, text, and messaging feedback
- ✅ Translation layer with safe fallback (verified with live API + offline mode)
- ✅ RAG retrieval — verified queries return correctly ranked, relevant results
- ✅ Rule-based prioritization into ranked demand hotspots
- ✅ Live Gemini-generated policymaker briefings, grounded in real report data
- ✅ Whisper voice transcription, confirmed accurate on real audio (`src/test_whisper.py`)
- ✅ Two-theme, fully responsive dashboard with live search

---

## Roadmap

1. **Real semantic embeddings** — upgrade retrieval from TF-IDF to production embeddings + a vector database (Chroma/Qdrant)
2. **Live voice pipeline** — wire the tested `transcribe_voice()` function directly into ingestion
3. **Persistent storage** — move from mock data to Supabase for continuous live feedback
4. **Multi-state rollout** — extend beyond pilot regions to a full state deployment

The architecture is built to scale without new code: new languages flow through the same translation layer, every channel feeds the same pipeline, and the same register works from a single ward to an entire state.

---

## Team

Built for *Build with AI: Code for Communities — Second Edition*, Theme: Innovation.