import streamlit as st
import pandas as pd
import plotly.express as px

# Load dataset
df = pd.read_csv("bank-additional-full copy.csv", sep=";", encoding="latin1")
df.columns = df.columns.str.strip()

st.title("Interactive Bank Marketing Dashboard")

# Sidebar filters
st.sidebar.header("Filter Options")

age_range = st.sidebar.slider(
    "Select Age Range:",
    int(df["age"].min()),
    int(df["age"].max()),
    (int(df["age"].min()), int(df["age"].max()))
)

job_options = st.sidebar.multiselect(
    "Select Job Types:",
    df["job"].unique(),
    default=df["job"].unique()
)

# Filter data
filtered = df[
    (df["age"] >= age_range[0]) &
    (df["age"] <= age_range[1]) &
    (df["job"].isin(job_options))
]

st.subheader("Filtered Data (first 10 rows)")
st.dataframe(filtered.head(10))

# Age distribution plot
st.subheader("Age Distribution")
fig1 = px.histogram(filtered, x="age", nbins=20, title="Age Distribution", 
                    color_discrete_sequence=px.colors.sequential.Plasma)
st.plotly_chart(fig1)

# Job counts plot
st.subheader("Job Counts")
job_counts = filtered["job"].value_counts().reset_index()
job_counts.columns = ["job", "count"]

fig2 = px.bar(
    job_counts,
    x="job",
    y="count",
    title="Job Frequency",
    color="count",
    color_continuous_scale=px.colors.sequential.Viridis
)
st.plotly_chart(fig2)

# Correlation heatmap
st.subheader("Correlation Heatmap (Numeric Columns)")
numeric_cols = filtered.select_dtypes(include="number")

if not numeric_cols.empty:
    fig3 = px.imshow(
        numeric_cols.corr(),
        text_auto=True,
        title="Correlation Heatmap",
        color_continuous_scale=px.colors.sequential.Cividis
    )
    st.plotly_chart(fig3)
else:
    st.write("Not enough numeric data to compute correlation.")
