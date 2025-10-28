import os
import re
import time
import json
import base64
import requests
import pandas as pd
from io import BytesIO
from PIL import Image
from typing import List, Tuple
from dotenv import load_dotenv

# === LOAD ENVIRONMENT VARIABLES FROM .env FILE ===
# Create a .env file in your project root with:
XAI_API_KEY="your_api_key_here"
EXCEL_PATH="path/to/sheet_dr.xlsx"
IMAGES_FOLDER="path/to/ct_scans"
OUTPUT_FILE="path/to/diagnosis_grok_results.xlsx"
load_dotenv()

# === CONFIGURATION ===
XAI_API_KEY = os.getenv("XAI_API_KEY")
XAI_API_URL = "https://api.x.ai/v1/chat/completions"

EXCEL_PATH = os.getenv("EXCEL_PATH", "input_data.xlsx")
IMAGES_FOLDER = os.getenv("IMAGES_FOLDER", "ct_scans")
OUTPUT_FILE = os.getenv("OUTPUT_FILE", "diagnosis_grok_results.xlsx")

# === FUNCTION TO ENCODE IMAGES ===
def encode_image_to_base64(image_path: str, max_size: Tuple[int, int] = (1024, 1024)) -> str:
    """Compress and encode image as base64 string for Grok API."""
    with Image.open(image_path) as img:
        img = img.convert("RGB")
        img.thumbnail(max_size)
        buffered = BytesIO()
        img.save(buffered, format="JPEG", quality=85)
        return base64.b64encode(buffered.getvalue()).decode("utf-8")

# === FUNCTION TO QUERY GROK API ===
def ask_grok(images_base64: List[str], medical_history: str = None) -> str:
    """Send CT images and context to Grok (xAI) API for simulated classification."""
    headers = {
        "Authorization": f"Bearer {XAI_API_KEY}",
        "Content-Type": "application/json"
    }

    # Prepare image content blocks
    image_contents = [
        {
            "type": "image_url",
            "image_url": {"url": f"data:image/jpeg;base64,{img}"}
        }
        for img in images_base64
    ]

    prompt = (
        "You are simulating a radiology assistant in a research context. "
        "Below are fictional CT scan images. Provide two **hypothetical classifications** using these categories:\n\n"
        "1 - Traumatische SAB\n"
        "2 - typische/atypische ICB\n"
        "3 - Kontusionsblutung\n"
        "4 - Aneurysmatische SAB\n"
        "5 - Andere Blutungen (Epidural-/Subduralblutung)\n\n"
        "For each classification, include:\n"
        "- The chosen category or categories\n"
        "- Brief reasoning (1–2 sentences)\n"
        "- Confidence level using Likert scale (1–5)\n\n"
        "⚠️ Important: This is not for medical use — only for academic analysis of AI reasoning in radiology.\n\n"
        f"1. Hypothetical classification **without medical history**.\n"
        f"2. Hypothetical classification **with medical history**: {medical_history or 'No history provided.'}"
    )

    payload = {
        "model": "grok-4-fast-reasoning",
        "messages": [
            {
                "role": "user",
                "content": [{"type": "text", "text": prompt}] + image_contents
            }
        ],
        "temperature": 0.3,
        "max_tokens": 2000
    }

    # Retry logic for transient API issues
    for attempt in range(3):
        try:
            response = requests.post(XAI_API_URL, headers=headers, json=payload, timeout=120)
            response.raise_for_status()
            data = response.json()
            return data["choices"][0]["message"]["content"]
        except requests.exceptions.RequestException as e:
            print(f"⚠️ API error (attempt {attempt + 1}/3): {e}")
            if attempt < 2:
                time.sleep(10)
        except (KeyError, IndexError, json.JSONDecodeError) as e:
            print(f"⚠️ Response parsing error: {e}")
            time.sleep(10)
    return "ERROR"

# === FUNCTION TO EXTRACT LIKERT SCORES ===
def extract_likert_scores(text: str) -> Tuple[any, any]:
    """Extract Likert scale (1–5) values from Grok output text."""
    scores = re.findall(r"(?:likert|confidence|skala)\s*[:\-]?\s*(\d{1,2})", text, re.IGNORECASE)
    scores = [int(s) for s in scores if 1 <= int(s) <= 5]

    if len(scores) >= 2:
        return int(scores[0]), int(scores[1])
    elif len(scores) == 1:
        return int(scores[0]), "N/A"
    return "N/A", "N/A"

# === MAIN PROCESSING FUNCTION ===
def process_excel_and_images():
    """Process Excel sheet, analyze CT scan images via Grok, and save results."""
    if not XAI_API_KEY:
        raise ValueError("❌ Missing XAI_API_KEY. Please set it in your .env file.")

    df = pd.read_excel(EXCEL_PATH)
    results = []

    print(f"🚀 Starting analysis for {len(df)} patients...")

    for idx, row in df.iterrows():
        patient_id = row["Reihenfolge Bilder"]
        medical_history = row.get("Anamnese (medical history)", "")

        print(f"\n🔍 Processing Patient{patient_id}...")

        image_paths = sorted([
            os.path.join(IMAGES_FOLDER, f)
            for f in os.listdir(IMAGES_FOLDER)
            if f.startswith(f"Patient{patient_id}_") and f.lower().endswith((".jpg", ".jpeg", ".png"))
        ])

        if not image_paths:
            print(f"⚠️ No images found for Patient{patient_id}")
            results.append({
                "Patient ID": patient_id,
                "Error": "No images found",
                "Grok Response": "",
                "Likert-Skala ohne Anamnese": "N/A",
                "Likert-Skala mit Anamnese": "N/A"
            })
            continue

        print(f"🖼️ Found {len(image_paths)} image(s)")

        try:
            encoded_images = [encode_image_to_base64(p) for p in image_paths]
        except Exception as e:
            print(f"❌ Image encoding failed: {e}")
            continue

        grok_response = ask_grok(encoded_images, medical_history)

        if grok_response == "ERROR":
            print(f"❌ Failed to get valid response for Patient{patient_id}")
            continue

        likert_no_hist, likert_with_hist = extract_likert_scores(grok_response)

        results.append({
            "Patient ID": patient_id,
            "Grok Response": grok_response,
            "Number of Images": len(image_paths),
            "Medical History": (
                medical_history[:200] + "..."
                if len(medical_history) > 200
                else medical_history
            ),
            "Likert-Skala ohne Anamnese": likert_no_hist,
            "Likert-Skala mit Anamnese": likert_with_hist
        })

        print(f"✅ Completed Patient{patient_id}")

    # Save all results
    out_df = pd.DataFrame(results)
    out_df.to_excel(OUTPUT_FILE, index=False)
    print(f"\n📁 Results saved to: {OUTPUT_FILE}")
    print(f"📊 Processed {len(results)} patients successfully.")

# === HELPER ===
def check_api_key() -> bool:
    """Verify that the API key is correctly set."""
    if not XAI_API_KEY:
        print("❌ Missing API key! Get one at https://console.x.ai/")
        print("Add it to your .env file as: XAI_API_KEY=your_api_key_here")
        return False
    return True

# === RUN SCRIPT ===
if __name__ == "__main__":
    if check_api_key():
        process_excel_and_images()
    else:
        print("⚠️ Please configure your API key before running.")
