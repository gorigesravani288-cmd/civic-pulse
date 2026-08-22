import whisper

print("Loading model (this may take a minute the first time)...")
model = whisper.load_model("base")

print("Transcribing...")
result = model.transcribe("test_audio.wav")  # change filename if different

print("\n--- TRANSCRIPT ---")
print(result["text"])