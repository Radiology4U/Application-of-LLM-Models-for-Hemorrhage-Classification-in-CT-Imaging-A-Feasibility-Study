import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import cohen_kappa_score
import textwrap
from dotenv import load_dotenv

# -------- LOAD ENVIRONMENT VARIABLES --------
load_dotenv()
excel_path = os.getenv("EXCEL_PATH", "input_data.xlsx")  # Set in .env or default fallback

# -------- COMPARISON SETTINGS --------
#YOU CAN INCLUDE ALL COLUMNS AT ONCE FOR THE PLOT
comparisons = [
    ("Befund der erfahr. Radiologen/Neuroradiologe ohne Anamnese", "Radiologist Prediction"),
    ("Befund der erfahr. Radiologen/Neuroradiologe mit Anamnese", "Radiologist Prediction"),
    ("Befund der erfahr. Radiologen/Neuroradiologe mit Anamnese", "Radiologist Prediction")
]

label_set = [1, 2, 3, 4, 5]  # Categories assumed to be encoded as 1–5, possibly multi-label with '+'

# -------- HELPER FUNCTIONS --------
def to_binary_vector(label_entry, label_set):
    """Convert a label entry (e.g., '2+4') to a binary vector like [0, 1, 0, 1, 0]."""
    if isinstance(label_entry, str):
        labels = list(map(int, label_entry.split('+')))
    else:
        labels = [int(label_entry)]
    return [1 if lbl in labels else 0 for lbl in label_set]

def compute_weighted_kappa_stats(true_col, pred_col):
    """Compute average Cohen's Kappa (quadratic-weighted) across all classes."""
    y_true_bin = np.array([to_binary_vector(val, label_set) for val in true_col])
    y_pred_bin = np.array([to_binary_vector(val, label_set) for val in pred_col])

    kappas = []
    for i in range(len(label_set)):
        kappa = cohen_kappa_score(y_true_bin[:, i], y_pred_bin[:, i], weights='quadratic')
        kappas.append(kappa)
    return np.mean(kappas), np.std(kappas)

# -------- LOAD DATA --------
df = pd.read_excel(excel_path)

# -------- COMPUTE KAPPA METRICS --------
comparison_names = []
kappa_means = []
kappa_errors = []

for col1, col2 in comparisons:
    mean_kappa, std_kappa = compute_weighted_kappa_stats(df[col1], df[col2])
    comparison_names.append(f"{col1} vs {col2}")
    kappa_means.append(mean_kappa)
    kappa_errors.append(std_kappa)

# -------- PLOT --------
fig, ax = plt.subplots(figsize=(10, 6))

wrapped_labels = ['\n'.join(textwrap.wrap(name, width=25)) for name in comparison_names]
hatch_styles = ['///', '\\\\', 'xxx']  # Visual distinction
bar_colors = ['white'] * len(kappa_means)

bars = ax.bar(
    wrapped_labels,
    kappa_means,
    yerr=kappa_errors,
    capsize=10,
    color=bar_colors,
    edgecolor='black',
    hatch=hatch_styles[:len(kappa_means)]
)

ax.set_ylim(0, 1)
ax.set_ylabel("Cohen Kappa")
ax.set_title("Cohen Kappa Agreement with Error Bars")
ax.yaxis.grid(True, linestyle='--', alpha=0.7)

for bar, score in zip(bars, kappa_means):
    height = bar.get_height()
    ax.text(
        bar.get_x() + bar.get_width() / 2,
        height + 0.02,
        f"{score:.2f}",
        ha='center',
        va='bottom',
        fontsize=10
    )

plt.tight_layout()
plt.show()
