import streamlit as st
import pandas as pd
import plotly.express as px

# Load dataset
df = pd.read_csv("bank-additional-full copy.csv", sep=";", encoding="latin1")
df.columns = df.columns.str.strip()

st.title("Bank Customer Insights & Marketing Optimization Dashboard")
st.write("Michael, Eleni, Leah - Group #22")

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

marital_options = st.sidebar.multiselect(
    "Select Marital Status:",
    df["marital"].unique(),
    default=df["marital"].unique()
)

education_options = st.sidebar.multiselect(
    "Select Education Level:",
    df["education"].unique(),
    default=df["education"].unique()
)

contact_options = st.sidebar.multiselect(
    "Select Contact Type:",
    df["contact"].unique(),
    default=df["contact"].unique()
)

# Filter data
filtered = df[
    (df["age"] >= age_range[0]) &
    (df["age"] <= age_range[1]) &
    (df["job"].isin(job_options)) &
    (df["marital"].isin(marital_options)) &
    (df["education"].isin(education_options)) &
    (df["contact"].isin(contact_options))
]

st.subheader("Summary Statistics")
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Total Customers", len(filtered))
with col2:
    avg_age = filtered["age"].mean()
    st.metric("Average Age", f"{avg_age:.1f}")
with col3:
    if "y" in filtered.columns:
        conversion_rate = (filtered["y"] == "yes").sum() / len(filtered) * 100
        st.metric("Conversion Rate", f"{conversion_rate:.1f}%")
    else:
        st.metric("N/A", "—")
with col4:
    if "y" in filtered.columns:
        converted = (filtered["y"] == "yes").sum()
        st.metric("Conversions", converted)
    else:
        st.metric("N/A", "—")

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
    st.write("Not enough numeric data to compute correlation."
            )         
