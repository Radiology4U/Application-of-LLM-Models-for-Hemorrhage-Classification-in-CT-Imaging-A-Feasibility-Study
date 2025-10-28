import os
import re
import time
import pandas as pd
from PIL import Image
from io import BytesIO
import google.generativeai as genai
from dotenv import load_dotenv

# === LOAD ENVIRONMENT VARIABLES FROM .env FILE ===
# Create a .env file in your project root with keys like:
GEMINI_API_KEY="your_api_key_here"
EXCEL_PATH="path/to/input_excel.xlsx"
IMAGES_FOLDER="path/to/images"
OUTPUT_FILE="path/to/save/output.xlsx"
load_dotenv()

# === CONFIGURATION ===
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
EXCEL_PATH = os.getenv("EXCEL_PATH", "input_data.xlsx")
IMAGES_FOLDER = os.getenv("IMAGES_FOLDER", "ct_scans")
OUTPUT_FILE = os.getenv("OUTPUT_FILE", "diagnosis_gemini_results.xlsx")

# Initialize Gemini API
genai.configure(api_key=GEMINI_API_KEY)

# === FUNCTION TO ENCODE IMAGES (WITH COMPRESSION) ===
def encode_image(image_path, max_size=(1024, 1024)):
    """Compress image and return raw bytes for Gemini input."""
    with Image.open(image_path) as img:
        img = img.convert("RGB")
        img.thumbnail(max_size)
        buffered = BytesIO()
        img.save(buffered, format="JPEG", quality=85)
        return buffered.getvalue()

# === FUNCTION TO QUERY GEMINI MULTIMODAL MODEL ===
def ask_gemini(images_bytes, medical_history=None):
    """Send images and patient history to Gemini for simulated classification."""
    model = genai.GenerativeModel("gemini-1.5-pro")

    prompt = (
        "You are simulating a radiology assistant in a research scenario. "
        "Below is a fictional case study involving CT images. "
        "Please provide two **hypothetical classifications** using the following categories:\n\n"
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

    # Retry loop to handle transient API issues
    for attempt in range(3):
        try:
            response = model.generate_content(
                contents=[prompt] + [genai.upload_image(img) for img in images_bytes],
                generation_config={"temperature": 0.3},
            )
            return response.text
        except Exception as e:
            print(f"⚠️ Error during Gemini call (attempt {attempt + 1}/3): {e}")
            time.sleep(10)
    return "ERROR"

# === FUNCTION TO EXTRACT LIKERT SCORES ===
def extract_likert_scores(text):
    """Extract Likert scale values (1–5) from model response text."""
    scores = re.findall(r'Likert[^:]*[:\-]?\s*([1-5])', text)
    if len(scores) == 2:
        return int(scores[0]), int(scores[1])
    elif len(scores) == 1:
        return int(scores[0]), "N/A"
    return "N/A", "N/A"

# === MAIN FUNCTION ===
def process_excel_and_images():
    """Read Excel data, process patient images, query Gemini, and save results."""
    df = pd.read_excel(EXCEL_PATH)
    results = []

    for idx, row in df.iterrows():
        patient_id = row["Reihenfolge Bilder"]
        medical_history = row.get("Anamnese (medical history)", "")

        print(f"\n🔍 Processing Patient{patient_id}")

        # Find matching images (e.g., Patient3_1.jpg, Patient3_2.jpg)
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
            print("📄 Medical history provided.")
        else:
            print("📄 No medical history.")

        encoded_images = [encode_image(p) for p in image_paths]

        g_response = ask_gemini(encoded_images, medical_history)

        if g_response == "ERROR":
            continue

        likert_no_hist, likert_with_hist = extract_likert_scores(g_response)

        results.append({
            "Patient ID": patient_id,
            "Combined Gemini Response": g_response,
            "Likert-Skala ohne Anamnese": likert_no_hist,
            "Likert-Skala mit Anamnese": likert_with_hist
        })

        print(f"✅ Diagnosis completed for Patient{patient_id}")

    # Save results to Excel
    out_df = pd.DataFrame(results)
    out_df.to_excel(OUTPUT_FILE, index=False)
    print(f"\n📁 Results saved to: {OUTPUT_FILE}")

# === RUN SCRIPT ===
if __name__ == "__main__":
    process_excel_and_images()
