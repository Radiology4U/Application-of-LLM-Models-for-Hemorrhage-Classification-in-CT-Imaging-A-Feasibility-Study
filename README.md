# 🧠 Application of GPT Models for Hemorrhage Classification in CT Imaging: A Feasibility Study

This repository investigates the potential of GPT models to assist in radiological decision-making by classifying CT scans for hemorrhage detection. The study simulates a realistic diagnostic setting, comparing GPT-based predictions with those of human raters at various levels of medical expertise.

---

## 📊 Study Overview

A total of **8 human raters** and **GPT-4o** participated in the classification of head CT scans. Each participant reviewed scans **twice**:

1. **Without access to medical history**
2. **With access to medical history**

For each case, raters:

* Assigned hemorrhage categories (**1 to 5**, multiple allowed)
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
├── chatgpt_prediction.py         # Generates GPT-based predictions from CT images
├── requirements.txt              # All required Python libraries
├── sample.env                    # Sample .env file for environment variables
├── plots/                        # Contains all plotting scripts
│   ├── cohen_kappa_plots.py      # Agreement visualization (Kappa scores)
│   └── likert_plots.py           # Likert boxplots for rater confidence
└── README.md                     # ← This file
```

---

## 🚀 Getting Started

### 🧰 Step 1: Clone the Repository

```bash
git clone https://github.com/your-repo-name
cd your-repo-name
```

### 📦 Step 2: Install Dependencies

```bash
pip install -r requirements.txt
```

### ⚙️ Step 3: Configure Environment

Create a `.env` file based on `sample.env`:

```
KAPPA_EXCEL_PATH=/absolute/path/to/input_data.xlsx
OPENAI_API_KEY=sk-...  # Needed only for GPT inference
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

* Hemorrhage labels (multi-label: 1–5)
* Medical history (text)
* Likert confidence scores for each rater under both conditions

---

## 🔐 Environment Variables

Stored locally in `.env`:

```
KAPPA_EXCEL_PATH=./input_data.xlsx
OPENAI_API_KEY=sk-...  # Required for GPT inference
```

---

## 💡 Notes

* Uses **synthetic/anonymized data**
* Intended **for academic research only**
* GPT outputs are **simulated**, not for clinical use

---

## 📢 Contact

For issues, contributions, or collaboration:

* 🛠️ Open a GitHub Issue
* 📧 See my profile on GitHub

---

## 📃 License

Licensed for **academic, non-clinical research use only**.

---

Made with ❤️ for responsible AI in healthcare.
