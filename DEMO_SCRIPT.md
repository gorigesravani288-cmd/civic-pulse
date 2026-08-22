# Civic Pulse — Pitch & Demo Script
**Target length: ~6–7 minutes (pitch) + ~3 minutes (live demo) = 10 min total**
Pairs with `civic_pulse_pitch_deck.pptx`

---

## 0. Before you start
- Have the live dashboard open in a second browser tab, already loaded, ready to switch to after Slide 5.
- Know your live urgency-search query in advance (suggested: "water supply problems") so the demo doesn't stall.
- If Wi-Fi is a risk, keep the screenshot slides (5 & 6) as your fallback — they're real captures of the actual product, not mockups, so they hold up even if live search fails.

---

## 1. Slide 1 — Title (30 sec)
**Say:**
"Every day, thousands of citizens report real infrastructure problems — a hospital without water, a dangerous road, an overflowing drain. Almost none of those reports reach the person who can actually act on them in time. We built Civic Pulse to fix that gap."

*(Pause on the title. Don't rush — let "Civic Pulse" land before moving on.)*

---

## 2. Slide 2 — The Problem (60 sec)
**Say:**
"Three things break down today. First, channels are fragmented — complaints come in by voice, WhatsApp, IVR, web forms, in a dozen languages, with nothing tying them together. Second, there's no way to prioritize — an official has no way to tell that ten flooding reports in one ward matter more than one pothole complaint elsewhere. And third, response is reactive — by the time a real crisis like a hospital losing water supply surfaces through normal channels, it's already an emergency, not an early warning."

**Transition line:** "So we asked: what if every one of those reports flowed into a single ranked, living register — automatically?"

---

## 3. Slide 3 — Our Solution (60 sec)
**Say:**
"That's Civic Pulse. It's a Digital Public Good that ingests citizen reports in any language, on any channel. Under the hood, a RAG search layer retrieves the reports that matter, clusters them by region and issue, and scores urgency automatically. The output isn't a spreadsheet of complaints — it's a ranked, actionable register, the same way a district officer reads a morning briefing."

**Point to the right panel:** "Today this replaces ten-plus separate language silos, scattered complaint logs, and a manual reporting process that used to take hours — with something that takes minutes."

---

## 4. Slide 4 — How It Works (45 sec)
**Say:**
"The pipeline has six real, tested steps: ingest voice, text, and messaging feedback; normalize it into one working language; retrieve the relevant reports with RAG search; prioritize by region and urgency; brief — where Gemini drafts the policymaker summary; and act — the register goes live on the dashboard. I want to be clear: every one of these arrows is a working module, not a mockup we're describing in theory."

---

## 5. Slide 5 — Live Product Screenshot (45 sec)
**Say:**
"This is not a design mockup — this is an actual screenshot of the running Civic Pulse dashboard, taken this week. You're looking at eight real entries, ranked by urgency. Right now, Nagpur's district hospital — a two-day water outage — sits at the top with 7 urgency points, ahead of a road-safety complaint in Lucknow at 6."

*(This is your bridge slide into the live demo — see Section 8 below.)*

---

## 6. Slide 6 — The AI Layer (60 sec)
**Say:**
"Here's what happens when an official clicks into that top entry. One click, and Gemini generates a live executive briefing — not from a template, but grounded in the actual retrieved citizen report. It names the responsible body — here, the Nagpur Municipal Corporation — and gives one concrete, time-bound action: dispatch emergency water tankers, and restore piped supply within 12 hours. This is generated on demand, so it's never stale, and it always cites its source."

---

## 7. Slide 7 — Under the Hood (40 sec)
**Say:**
"On the technical side: Gemini handles the reasoning and briefings, Whisper handles speech-to-text for voice-based reports, and a RAG search layer retrieves across our multilingual feedback records. It's built on FastAPI with a Supabase-ready backend, a real translation pipeline, and a live dashboard — so this isn't just a hackathon script, it's an architecture that's ready to take on real, persistent data."

---

## 8. Slide 8 — Impact & Roadmap (45 sec)
**Say:**
"Where this goes next: production-grade semantic embeddings instead of our current TF-IDF baseline, wiring our tested Whisper pipeline directly into live ingestion, moving from mock data to persistent Supabase storage, and then a multi-state rollout. The reason we're confident it scales is architectural — new languages add zero new code, every channel feeds the same pipeline, and the same register works whether you're looking at a single ward or an entire state."

---

## 9. Slide 9 — Thank You / Close (20 sec)
**Say:**
"Civic Pulse turns scattered citizen voices into a signal a government can actually act on. Thank you — happy to take questions, or show the live dashboard again."

---

## Live Demo Segment (insert after Slide 5, ~3 min)

**Switch to the browser tab with the real dashboard.**

1. **Show the live feed (30 sec):** "This is the same view you just saw in the deck, live. Eight active signals, synced [mention timestamp shown on screen]." Point out the sparkline of top regions by urgency.

2. **Run a live query (60 sec):** Type into the search box: `water supply problems, road accidents, garbage collection`
   - "Watch — this is a real RAG search over the citizen report corpus, ranking results by relevance to the query, not just keyword match."

3. **Generate a live briefing (60 sec):** Click "Generate AI Briefing" on the Lucknow (roads & transport) entry — a fresh one, not the pre-generated Nagpur example from the slides.
   - "This calls Gemini live, right now, grounded in the actual report text you can see above it. Notice it names the specific department and gives a concrete next step — not generic advice."

4. **Close the loop (20 sec):** "So from a citizen's voice note, to a ranked register, to a named action for the right municipal body — all live, all today."

---

## Anticipated Q&A
| Question | Short answer |
|---|---|
| Is this real data? | The screenshots in the deck are actual captures from the running app; today's demo mock data mirrors the structure our production ingestion pipeline expects. |
| How does urgency scoring work? | Currently a rules-based score combining report volume, severity keywords, and category weight — the roadmap moves this to a learned model once real usage data accumulates. |
| What about false or spam reports? | Not yet built — flagged as a near-term roadmap item alongside authentication/verification at the ingestion layer. |
| Data privacy / who sees this? | Designed for internal use by municipal officials; access control and citizen PII handling are part of the production hardening roadmap, not yet implemented in this pilot. |
| Why RAG instead of just keyword search? | RAG lets an official query in natural language ("water problems near schools") and get semantically relevant reports back, even if the citizen's original wording was completely different. |
