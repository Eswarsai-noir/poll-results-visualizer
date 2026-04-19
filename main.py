import pandas as pd
import numpy as np

# ===============================
# STEP 1: GENERATE SYNTHETIC DATA
# ===============================

np.random.seed(42)
n = 500

df = pd.DataFrame({
    "Respondent_ID": range(1, n+1),
    "Date": pd.date_range(start="2024-01-01", periods=n, freq="D"),
    "Region": np.random.choice(["North", "South", "East", "West"], n),
    "Age_Group": np.random.choice(["18-25", "26-35", "36-50"], n),
    "Gender": np.random.choice(["Male", "Female"], n),
    "Option_Selected": np.random.choice(
        ["Product A", "Product B", "Product C"],
        n,
        p=[0.4, 0.35, 0.25]
    )
})

df.to_csv("data/poll_data.csv", index=False)

print("✅ Synthetic poll data generated successfully at data/poll_data.csv!")

# ===============================
# STEP 2: INSIGHT FUNCTION
# ===============================

def generate_insights(df):
    insights = []

    top = df["Option_Selected"].value_counts().idxmax()
    insights.append(f"Top preferred product is {top}")

    region_pref = df.groupby("Region")["Option_Selected"].agg(
        lambda x: x.value_counts().index[0]
    )

    for r, p in region_pref.items():
        insights.append(f"In {r}, most preferred is {p}")

    return insights

# ===============================
# STEP 3: RUN ANALYSIS
# ===============================

insights = generate_insights(df)

print("\n📊 Insights:")
for i in insights:
    print("-", i)
