"""
Step 1: Data Ingestion Layer
Loads raw citizen feedback (text/voice-transcribed/messaging) from a source.
In production: replace load_mock_feedback() with real connectors
(WhatsApp Business API, IVR + Whisper transcription, web form submissions, etc.)
"""

import json
import os


DATA_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "mock_feedback.json")

_whisper_model = None


def load_mock_feedback():
    """Load citizen feedback records. Swap this for a real DB/API call later."""
    with open(DATA_PATH, "r", encoding="utf-8") as f:
        records = json.load(f)
    return records


def transcribe_voice(audio_path: str) -> str:
    """
    Transcribes an audio file to text using OpenAI's Whisper model.
    Loads the model once and reuses it across calls for efficiency.

    Whisper is imported lazily here (not at module load time) so that
    deploying the backend API doesn't require installing PyTorch — it's
    only needed if this function is actually called.

    Tested and confirmed working — see test_whisper.py for a standalone
    example. Not yet wired into the live mock pipeline since demo data is
    pre-transcribed for speed, but this function is ready to plug in:
    just pass it a real audio file path from voice-based citizen feedback.
    """
    global _whisper_model
    if _whisper_model is None:
        import whisper
        _whisper_model = whisper.load_model("base")
    result = _whisper_model.transcribe(audio_path)
    return result["text"].strip()


if __name__ == "__main__":
    records = load_mock_feedback()
    print(f"Loaded {len(records)} feedback records\n")
    for r in records[:3]:
        print(f"[{r['id']}] ({r['region']}, lang={r['language']}, via={r['channel']})")
        print(f"  {r['text']}\n")