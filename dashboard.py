import streamlit as st
import pandas as pd
import plotly.express as px

# -------------------------
# Load Data
# -------------------------
df = pd.read_csv("bank-additional-full copy.csv", sep=';', encoding='latin1')
df.columns = df.columns.str.strip()  # clean column names

# -------------------------
# Page Title
# -------------------------
st.markdown(
    "<h1 style='text-align:center; font-weight:bold;'>Interactive Bank Dashboard</h1>",
    unsafe_allow_html=True
)

# -------------------------
# Sidebar Filters
# -------------------------

st.sidebar.header("Filter Options")

# Age slider
min_age = int(df['age'].min())
max_age = int(df['age'].max())

age_range = st.sidebar.slider(
    "Select Age Range:",
    min_value=min_age,
    max_value=max_age,
    value=(min_age, max_age)
)

# Job multiselect
job_options = df['job'].unique().tolist()

selected_jobs = st.sidebar.multiselect(
    "Select Job Types:",
    options=job_options,
    default=job_options
)

# -------------------------
# Apply Filters
# -------------------------
filtered = df[
    (df['age'] >= age_range[0]) &
    (df['age'] <= age_range[1]) &
    (df['job'].isin(selected_jobs))
]

st.write(f"### Showing {len(filtered)} matching customers")

# -------------------------
# Show Data Preview
# -------------------------
st.write("#### Filtered Data Sample")
st.dataframe(filtered.head(10))

# -------------------------
# Age Distribution Plot
# -------------------------
st.write("### Age Distribution")
fig1 = px.histogram(
    filtered,
    x='age',
    nbins=20,
    color_discrete_sequence=px.colors.sequential.Plasma,
)
st.plotly_chart(fig1, use_container_width=True)

# -------------------------
# Job Count Plot
# -------------------------
st.write("### Job Counts")
job_counts = filtered['job'].value_counts().reset_index()
job_counts.columns = ['job', 'count']

fig2 = px.bar(
    job_counts,
    x='job',
    y='count',
    color='count',
    color_continuous_scale=px.colors.sequential.Viridis,
)
st.plotly_chart(fig2, use_container_width=True)

# -------------------------
# Correlation Heatmap
# -------------------------
numeric_cols = filtered.select_dtypes(include='number')

if numeric_cols.empty:
    st.write("Not enough numeric data for heatmap.")
else:
    st.write("### Correlation Heatmap")
    fig3 = px.imshow(
        numeric_cols.corr(),
        text_auto=True,
        color_continuous_scale=px.colors.sequential.Cividis,
    )
    st.plotly_chart(fig3, use_container_width=True)
