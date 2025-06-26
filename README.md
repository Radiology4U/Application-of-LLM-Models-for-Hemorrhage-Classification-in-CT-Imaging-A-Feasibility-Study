# 🧠 Application of GPT Models for Hemorrhage Classification in CT Imaging: A Feasibility Study

This repository investigates the potential of GPT models to assist in radiological decision-making by classifying CT scans for hemorrhage detection. The study simulates a realistic diagnostic setting, comparing GPT-based predictions with those of human raters at various levels of medical expertise.

---

## 📊 Study Overview

A total of **47 patients** were included in this study. **8 human raters** and **GPT-4o** participated in the classification of head CT scans. Each participant reviewed scans **twice**:

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
├── chatgpt\_prediction.py         # Generates GPT-based predictions from CT images
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
OPENAI_API_KEY=sk-...
EXCEL_PATH=/path/to/input_data.xlsx
IMAGES_FOLDER=/path/to/ct_scans
OUTPUT_FILE=/path/to/diagnosis_results.xlsx
```

### ▶️ Step 4: Run Scripts

* **Generate GPT predictions**
  `python chatgpt_prediction.py`

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
OPENAI_API_KEY=sk-...
EXCEL_PATH=/path/to/input_data.xlsx
IMAGES_FOLDER=/path/to/ct_scans
OUTPUT_FILE=/path/to/diagnosis_results.xlsx
```

---

## 💡 Notes

* Dataset includes **47 patients**
* Intended **for academic research only**
* This is a feasibility study — **not for clinical use**
* GPT-4o does not directly interpret images — predictions are made via structured prompts using metadata or textual imaging findings

---

## 📢 Contact

For issues, contributions, or collaboration:

* 🛠️ Open a GitHub Issue

---

## 📃 License



---

Made with ❤️ for responsible AI in healthcare.
