import os
from pathlib import Path
from dotenv import load_dotenv

env_path = Path(__file__).resolve().parent / ".env"
print("Looking for .env at:", env_path)
print("Does it exist?:", env_path.exists())

load_dotenv(dotenv_path=env_path)

key = os.getenv("GEMINI_API_KEY")
print("Key found?:", bool(key))
if key:
    print("Key starts with:", key[:6])