import argparse
import json
import base64
import os
from dotenv import load_dotenv
import google.generativeai as genai
from verifier import verify_transactions
from prompts import UNIVERSAL_PROMPT

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel("gemini-1.5-flash")


def encode_file(file_path):
    with open(file_path, "rb") as f:
        return base64.b64encode(f.read()).decode()


def call_model(file_path, retry_context=None):
    file_data = encode_file(file_path)

    prompt = UNIVERSAL_PROMPT
    if retry_context:
        prompt += f"\nFix this error:\n{retry_context}"

    response = model.generate_content([
        prompt,
        {"mime_type": "image/png", "data": file_data}
    ])

    return response.text


def extract(file_path):
    for attempt in range(3):
        print(f"Attempt {attempt+1}...")

        raw = call_model(file_path)
        data = json.loads(raw)

        valid, msg = verify_transactions(data)

        if valid:
            print("✓ Verification Passed")
            return data
        else:
            print("✗ Failed:", msg)
            raw = call_model(file_path, retry_context=msg)

    return {"error": "Verification failed after retries"}


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--file", required=True)
    args = parser.parse_args()

    result = extract(args.file)
    print(json.dumps(result, indent=2))
