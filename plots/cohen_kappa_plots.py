import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import cohen_kappa_score
import textwrap
from dotenv import load_dotenv
from matplotlib.patches import Patch

# -------- LOAD ENVIRONMENT VARIABLES --------
load_dotenv()
excel_path = os.getenv("EXCEL_PATH", "input_data.xlsx")  # Default path if not in .env

# -------- COMPARISON PAIRS --------
comparisons = [
    ("Student-1-without-medical history", "Radiologist Prediction"),
    ("Student-1-with-medical history", "Radiologist Prediction"),
    ("Student-2-without-medical history", "Radiologist Prediction"),
    ("Student-2-with-medical history", "Radiologist Prediction"),
    ("Student-3-without-medical history", "Radiologist Prediction"),
    ("Student-3-with-medical history", "Radiologist Prediction"),
    ("Student-4-without-medical history", "Radiologist Prediction"),
    ("Student-4-with-medical history", "Radiologist Prediction"),
    ("Resident-1-without-medical history", "Radiologist Prediction"),
    ("Resident-1-with-medical history", "Radiologist Prediction"),
    ("Resident-2-without-medical history", "Radiologist Prediction"),
    ("Resident-2-with-medical history", "Radiologist Prediction"),
    ("Expert-without-medical history", "Radiologist Prediction"),
    ("Expert-with-medical history", "Radiologist Prediction"),
    ("GPT-4o-without-medical history", "Radiologist Prediction"),
    ("GPT-4o-with-medical history", "Radiologist Prediction"),
    ("gemini-2.5-flash-without-medical history", "Radiologist Prediction"),
    ("gemini-2.5-flash-with-medical history", "Radiologist Prediction"),
    ("grok-4-fast-reasoning-without-medical history", "Radiologist Prediction"),
    ("grok-4-fast-reasoning-with-medical history", "Radiologist Prediction"),
]

label_set = [1, 2, 3, 4, 5]

# -------- HELPER FUNCTIONS --------
def to_binary_vector(label_entry, label_set):
    """Convert label string like '2+3' to binary vector [0,1,1,0,0]."""
    if isinstance(label_entry, str):
        labels = list(map(int, label_entry.split('+')))
    else:
        labels = [int(label_entry)]
    return [1 if lbl in labels else 0 for lbl in label_set]

def compute_weighted_kappa_stats(true_col, pred_col):
    """Compute average Cohen's Kappa across all binary categories."""
    y_true_bin = np.array([to_binary_vector(val, label_set) for val in true_col])
    y_pred_bin = np.array([to_binary_vector(val, label_set) for val in pred_col])

    kappas = []
    for i in range(len(label_set)):
        kappa = cohen_kappa_score(y_true_bin[:, i], y_pred_bin[:, i], weights='quadratic')
        kappas.append(kappa)
    return np.mean(kappas), np.std(kappas)

# -------- LOAD DATA & CALCULATE METRICS --------
df = pd.read_excel(excel_path)
comparison_names = []
kappa_means = []
kappa_errors = []

for col1, col2 in comparisons:
    mean_kappa, std_kappa = compute_weighted_kappa_stats(df[col1], df[col2])
    comparison_names.append(f"{col1} vs {col2}")
    kappa_means.append(mean_kappa)
    kappa_errors.append(std_kappa)

# -------- PLOT HORIZONTAL BARS --------
fig, ax = plt.subplots(figsize=(12, 10))

# Wrap long labels
wrapped_labels = ['\n'.join(textwrap.wrap(name, width=50)) for name in comparison_names]

# Alternate colors for without/with history
bar_colors = ['gold' if i % 2 == 0 else 'royalblue' for i in range(len(kappa_means))]

# Draw bars with error bars
bars = ax.barh(
    wrapped_labels,
    kappa_means,
    xerr=kappa_errors,
    capsize=6,
    color=bar_colors,
    edgecolor='black'
)

# Annotate values
for bar, score in zip(bars, kappa_means):
    width = bar.get_width()
    ax.text(
        width + 0.015,
        bar.get_y() + bar.get_height() / 2,
        f"{score:.2f}",
        ha='left',
        va='center',
        fontsize=9
    )

# Aesthetics
ax.set_xlim(0, 1)
ax.set_xlabel("Cohen Kappa", fontsize=12)
ax.set_title("Cohen Kappa Agreement with Error Bars", fontsize=14)
ax.set_yticklabels(wrapped_labels, fontsize=9)
ax.xaxis.grid(True, linestyle='--', alpha=0.7)

# Add legend
legend_elements = [
    Patch(facecolor='gold', edge
