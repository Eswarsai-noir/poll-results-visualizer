import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# ===============================
# PAGE CONFIG
# ===============================
st.set_page_config(page_title="Poll Results Visualizer", layout="wide")
st.title("📊 Poll Results Visualizer (No Plotly Version)")

# ===============================
# LOAD DATA
# ===============================
@st.cache_data
def load_data():
    df = pd.read_csv("data/poll_data.csv")
    df["Date"] = pd.to_datetime(df["Date"])
    return df

df = load_data()

# ===============================
# FILTERS
# ===============================
st.sidebar.header("🔍 Filters")

region = st.sidebar.multiselect(
    "Region",
    df["Region"].unique(),
    df["Region"].unique()
)

age = st.sidebar.multiselect(
    "Age Group",
    df["Age_Group"].unique(),
    df["Age_Group"].unique()
)

gender = st.sidebar.multiselect(
    "Gender",
    df["Gender"].unique(),
    df["Gender"].unique()
)

filtered_df = df[
    (df["Region"].isin(region)) &
    (df["Age_Group"].isin(age)) &
    (df["Gender"].isin(gender))
]

# ===============================
# KPI METRICS
# ===============================
st.subheader("📌 Key Metrics")

col1, col2, col3 = st.columns(3)
col1.metric("Total Responses", len(filtered_df))
col2.metric("Regions", filtered_df["Region"].nunique())
col3.metric("Options", filtered_df["Option_Selected"].nunique())

# ===============================
# VOTE DISTRIBUTION (BAR CHART)
# ===============================
st.subheader("📊 Vote Distribution")

vote_counts = filtered_df["Option_Selected"].value_counts().reset_index()
vote_counts.columns = ["Option", "Votes"]

fig, ax = plt.subplots()
sns.barplot(data=vote_counts, x="Option", y="Votes", ax=ax)
ax.set_title("Votes per Option")

st.pyplot(fig)

# ===============================
# PIE CHART
# ===============================
st.subheader("🥧 Vote Share")

fig2, ax2 = plt.subplots()
ax2.pie(
    vote_counts["Votes"],
    labels=vote_counts["Option"],
    autopct="%1.1f%%"
)
ax2.set_title("Vote Share")

st.pyplot(fig2)

# ===============================
# TREND ANALYSIS
# ===============================
st.subheader("📈 Trend Analysis")

trend = filtered_df.groupby(["Date", "Option_Selected"]).size().reset_index(name="Count")

fig3, ax3 = plt.subplots(figsize=(10, 5))
sns.lineplot(data=trend, x="Date", y="Count", hue="Option_Selected", ax=ax3)
ax3.set_title("Trend Over Time")

st.pyplot(fig3)

# ===============================
# AGE ANALYSIS
# ===============================
st.subheader("👥 Age Group Analysis")

age_data = pd.crosstab(filtered_df["Age_Group"], filtered_df["Option_Selected"])

fig4, ax4 = plt.subplots()
age_data.plot(kind="bar", stacked=True, ax=ax4)
ax4.set_title("Age Group Preference")

st.pyplot(fig4)

# ===============================
# REGION ANALYSIS
# ===============================
st.subheader("🌍 Region Analysis")

region_data = pd.crosstab(filtered_df["Region"], filtered_df["Option_Selected"])

fig5, ax5 = plt.subplots()
region_data.plot(kind="bar", stacked=True, ax=ax5)
ax5.set_title("Region-wise Preferences")

st.pyplot(fig5)

# ===============================
# INSIGHTS
# ===============================
st.subheader("💡 Insights")

def generate_insights(df):
    insights = []

    if len(df) == 0:
        return ["No data available"]

    top = df["Option_Selected"].value_counts().idxmax()
    insights.append(f"🏆 Top product: {top}")

    region_pref = df.groupby("Region")["Option_Selected"].agg(
        lambda x: x.value_counts().index[0]
    )

    for r, p in region_pref.items():
        insights.append(f"📍 {r}: {p}")

    return insights

for i in generate_insights(filtered_df):
    st.write(i)

# ===============================
# DATA PREVIEW
# ===============================
st.subheader("📄 Data Preview")
st.dataframe(filtered_df.head())