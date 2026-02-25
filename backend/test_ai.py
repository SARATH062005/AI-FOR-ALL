import os
import requests
import json
from dotenv import load_dotenv

load_dotenv()

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

def test_ai():
    print(f"Testing OpenRouter API with key: {OPENROUTER_API_KEY[:5]}...{OPENROUTER_API_KEY[-5:] if OPENROUTER_API_KEY else 'None'}")
    
    if not OPENROUTER_API_KEY or "your_key_here" in OPENROUTER_API_KEY:
        print("❌ Error: OpenRouter API key is not set or is still the placeholder.")
        return

    prompt = "Hello, can you hear me? Respond with a short JSON like {'status': 'ok'}"
    
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": "google/gemini-2.0-flash-001",
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "response_format": { "type": "json_object" }
    }

    try:
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers=headers,
            data=json.dumps(payload),
            timeout=10
        )
        print(f"Status Code: {response.status_code}")
        if response.status_code == 200:
            print("✅ AI Connection Successful!")
            print(f"Response: {response.json()['choices'][0]['message']['content']}")
        else:
            print(f"❌ AI Connection Failed: {response.text}")
    except Exception as e:
        print(f"❌ Network Error: {e}")

if __name__ == "__main__":
    test_ai()
