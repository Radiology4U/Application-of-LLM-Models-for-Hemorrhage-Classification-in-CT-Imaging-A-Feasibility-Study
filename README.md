# 🧠 Application of LLM Models for Hemorrhage Classification in CT Imaging: A Feasibility Study

This project explores the use of advanced multimodal Large Language Models (LLMs) GPT-4o, Gemini 2.5 Flash, and Grok 4 Fast Reasoning to classify CT scan images for potential hemorrhage detection and generate diagnostic summaries. The goal is to evaluate the feasibility, consistency, and interpretability of LLM-driven image-based clinical reasoning.

---

## 📊 Study Overview

A total of **47 patients** were included in this study. **8 human raters** and **GPT-4o, Gemini 2.5 Flash, Grok 4 Fast Reasoning** participated in the classification of head CT scans. Each participant reviewed scans **twice**:

1. **Without access to medical history**
2. **With access to medical history**

For each case, raters:

* Assigned hemorrhage categories (one or more of the following):
  - **1** – Traumatische SAB (traumatic subarachnoid hemorrhage)
  - **2** – typische/atypische ICB (typical/atypical intracerebral hemorrhage)
  - **3** – Kontusionsblutung (contusional hemorrhage)
  - **4** – Aneurysmatische SAB (aneurysmal subarachnoid hemorrhage)
  - **5** – Andere Blutungen (epidural/subdural hemorrhage)
* Provided a **confidence score** (1–5 Likert scale)

These outputs were used to compute inter-rater agreement and confidence shifts across different context conditions.

---

## 🕵️ Raters Involved

* 👩‍⚕️ **4 Medical Students** (Student 1–4)
* 🩻 **2 Radiology Residents**
* 🧠 **1 Head of Department (Expert)**
* 🤖 **GPT-4o (ChatGPT)**
* 🤖 **gemini-2.5-flash (Gemini)**
* 🤖 **grok-4-fast-reasoning (Grok)**
  
---

## 📈 Evaluation Metrics

### ✅ 1. **Cohen’s Kappa**

* Measures agreement between each rater and the expert radiologist (ground truth)
* Supports **multi-label classification**
* Visualized as a **horizontal bar plot** with error bars

### 🎯 2. **Likert Confidence Ratings**

* Confidence scores reported on a **Likert scale (1 = low, 5 = high)**
* Visualized using a **boxplot**, split by:

  * **Without history**
  * **With history**

---

## 📁 Repository Structure

```

.
├── predictions/                        # Contains codes for getting predictions out of LLM's
│   ├── GPT4o_prediction.py     
│   └── gemini_prediction.py
│   └── Grok_prediction.py                  
├── requirements.txt              # All required Python libraries
├── sample.env                    # Sample .env file for environment variables
├── plots/                        # Contains all plotting scripts
│   ├── cohen\_kappa\_plots.py      # Agreement visualization (Kappa scores)
│   └── likert\_plots.py           # Likert boxplots for rater confidence
└── README.md                     # ← This file

````

---

## 🚀 Getting Started

### 🧰 Step 1: Clone the Repository

```bash
git clone https://github.com/your-repo-name
cd your-repo-name
````

### 📦 Step 2: Install Dependencies

```bash
pip install -r requirements.txt
```

### ⚙️ Step 3: Configure Environment

Create a `.env` file based on `sample.env`:

```
OPENAI_API_KEY=sk-your_openai_api_key_here
GEMINI_API_KEY=your_gemini_api_key_here
GROK_API_KEY=your_grok_api_key_here
EXCEL_PATH=/path/to/input_data.xlsx
IMAGES_FOLDER=/path/to/ct_scans
OUTPUT_FILE=/path/to/diagnosis_results.xlsx
```

### ▶️ Step 4: Run Scripts

* **Generate GPT-4o predictions**  
  `python predictions/GPT4o_prediction.py`

* **Generate Gemini 2.5 Flash predictions**  
  `python predictions/gemini_prediction.py`

* **Generate Grok 4 Fast Reasoning predictions**  
  `python predictions/Grok_prediction.py`

* **Plot Cohen’s Kappa agreement**
  `python plots/cohen_kappa_plots.py`

* **Plot Likert confidence scores**
  `python plots/likert_plots.py`

---

## 📄 Input Format

### 🖼️ CT Scan Slices

* JPEG images named like `Patient<ID>_X.jpg`

### 📊 Excel Metadata (`input_data.xlsx`)

* Patient-level metadata including:

  * Hemorrhage labels (multi-label: categories 1–5 as below)
  * Medical history (text)
  * Likert confidence scores for each rater under both conditions

#### 🩸 Hemorrhage Categories

| Code | Description                            |
| ---- | -------------------------------------- |
| 1    | Traumatische SAB (Traumatic SAH)       |
| 2    | typische/atypische ICB (Intracerebral) |
| 3    | Kontusionsblutung (Contusional)        |
| 4    | Aneurysmatische SAB (Aneurysmal SAH)   |
| 5    | Andere Blutungen (Epi-/Subdural)       |

---

## 🔐 Environment Variables

Stored locally in `.env`:

```
OPENAI_API_KEY=sk-your_openai_api_key_here
GEMINI_API_KEY=your_gemini_api_key_here
GROK_API_KEY=your_grok_api_key_here
EXCEL_PATH=/path/to/input_data.xlsx
IMAGES_FOLDER=/path/to/ct_scans
OUTPUT_FILE=/path/to/diagnosis_results.xlsx
```

---

## 💡 Notes

* Dataset includes **47 patients**
* Intended **for academic research only**
* This is a feasibility study — **not for clinical use**

---

## 📢 Contact

For issues, contributions, or collaboration:

* 🛠️ Open a GitHub Issue

---

## 📃 License



---

Made with ❤️ for responsible AI in healthcare.
