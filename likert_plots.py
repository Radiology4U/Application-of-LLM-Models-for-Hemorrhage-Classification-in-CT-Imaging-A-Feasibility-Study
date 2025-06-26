import os
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from dotenv import load_dotenv

# -------- LOAD ENVIRONMENT VARIABLES --------
load_dotenv()
file_path = os.getenv("EXCEL_PATH", "input_data.xlsx")  # Default fallback

# -------- STEP 1: LOAD EXCEL FILE --------
df = pd.read_excel(file_path)

# -------- STEP 2: FILTER COLUMNS (With/Without Medical History) --------
rater_cols = [col for col in df.columns if 'With' in col or 'Without' in col]

# -------- STEP 3: TRANSFORM TO LONG FORMAT --------
df_long = df[rater_cols].melt(var_name='Rater_Condition', value_name='Confidence')

# -------- STEP 4: EXTRACT RATER AND CONDITION INFO --------
df_long[['Rater', 'Condition']] = df_long['Rater_Condition'].str.extract(r'(.+?)[ _](Without|With)', expand=True)

# Optional sanity check
# print(df_long.head())

# -------- STEP 5: BOXPLOT --------
plt.figure(figsize=(14, 6))
sns.boxplot(data=df_long, x='Rater', y='Confidence', hue='Condition', palette='Set2')
plt.xticks(rotation=45)
plt.ylabel('Confidence Score')
plt.title('Confidence Ratings by Rater (With vs Without Medical History)')
plt.tight_layout()
plt.show()
