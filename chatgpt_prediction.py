import os
import pandas as pd
import openai
from PIL import Image
import base64
from io import BytesIO
import time
import re
from dotenv import load_dotenv

# === LOAD ENVIRONMENT VARIABLES FROM .env FILE ===
load_dotenv()

# === CONFIGURATION ===
EXCEL_PATH = os.getenv("EXCEL_PATH", "input_data.xlsx")
IMAGES_FOLDER = os.getenv("IMAGES_FOLDER", "ct_scans")
OUTPUT_FILE = os.getenv("OUTPUT_FILE", "diagnosis_results.xlsx")
openai.api_key = os.getenv("OPENAI_API_KEY")  # Store this securely in a .env file

# === FUNCTION TO ENCODE IMAGES WITH COMPRESSION ===
def encode_image(image_path, max_size=(1024, 1024)):
    with Image.open(image_path) as img:
        img = img.convert("RGB")
        img.thumbnail(max_size)
        buffered = BytesIO()
        img.save(buffered, format="JPEG", quality=85)
        return base64.b64encode(buffered.getvalue()).decode()

# === FUNCTION TO QUERY GPT-4o WITH IMAGES ===
def ask_gpt(images_base64, medical_history=None):
    image_parts = [
        {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{img}"}}
        for img in images_base64
    ]

    prompt = (
        "You are simulating a radiology assistant in a research scenario. "
        "Below is a fictional case study involving CT images. "
        "Please provide two **hypothetical classifications** using the following categories (one classification can belong to multiple categories):\n\n"
        "1 - Traumatische SAB\n"
        "2 - typische/atypische ICB\n"
        "3 - Kontusionsblutung\n"
        "4 - Aneurysmatische SAB\n"
        "5 - Andere Blutungen (Epidural-/Subduralblutung)\n\n"
        "For each hypothetical classification, include:\n"
        "- The chosen category or categories\n"
        "- A brief reasoning (1–2 sentences)\n"
        "- Your confidence level (1–5 scale)\n\n"
        "Important: This is not for medical use and does not represent real patient data. "
        "It is purely for academic analysis of language model behavior in radiological contexts.\n\n"
        f"1. Hypothetical classification **without medical history**.\n"
        f"2. Hypothetical classification **with medical history**: {medical_history or 'No history provided.'}"
    )

    for attempt in range(3):
        try:
            response = openai.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "user", "content": [{"type": "text", "text": prompt}] + image_parts}
                ],
                max_tokens=1000
            )
            return response.choices[0].message.content
        except openai.RateLimitError:
            print("⚠️ Rate limit hit, retrying in 10 seconds...")
            time.sleep(10)
        except Exception as e:
            print(f"❌ Error during GPT call: {e}")
            break
    return "ERROR"

# === FUNCTION TO EXTRACT LIKERT SCORES ===
def extract_likert_scores(text):
    scores = re.findall(r'Likert[^:]*[:\-]?\s*([1-5])', text)
    if len(scores) == 2:
        return int(scores[0]), int(scores[1])
    elif len(scores) == 1:
        return int(scores[0]), "N/A"
    return "N/A", "N/A"

# === MAIN FUNCTION ===
def process_excel_and_images():
    df = pd.read_excel(EXCEL_PATH)
    results = []

    for idx, row in df.iterrows():
        patient_id = row["Reihenfolge Bilder"]
        medical_history = row.get("Anamnese (medical history)", "")

        print(f"\n🔍 Processing Patient{patient_id}")

        image_paths = sorted([
            os.path.join(IMAGES_FOLDER, f)
            for f in os.listdir(IMAGES_FOLDER)
            if f.startswith(f"Patient{patient_id}_") and f.endswith(".jpg")
        ])

        if not image_paths:
            print(f"⚠️ No images found for Patient{patient_id}")
            continue

        print(f"🖼️ Found {len(image_paths)} image(s) for Patient{patient_id}")

        if medical_history.strip():
            print(f"📄 Medical history provided.")
        else:
            print("📄 No medical history.")

        encoded_images = [encode_image(p) for p in image_paths]

        gpt_response = ask_gpt(encoded_images, medical_history)

        if gpt_response == "ERROR":
            continue

        likert_no_hist, likert_with_hist = extract_likert_scores(gpt_response)

        results.append({
            "Patient ID": patient_id,
            "Combined GPT Response": gpt_response,
            "Likert-Skala ohne Anamnese": likert_no_hist,
            "Likert-Skala mit Anamnese": likert_with_hist
        })

        print(f"✅ Diagnosis completed for Patient{patient_id}")

    out_df = pd.DataFrame(results)
    out_df.to_excel(OUTPUT_FILE, index=False)
    print(f"\n📁 Results saved to: {OUTPUT_FILE}")

# === RUN SCRIPT ===
if __name__ == "__main__":
    process_excel_and_images()
