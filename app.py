import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Page config
st.set_page_config(page_title="NFHS Dashboard", layout="wide")

# Title
st.title("📊 National Family Health Survey Dashboard")

# Load data
@st.cache_data
def load_data():
    df = pd.read_csv("All India National Family Health Survey.csv")
    return df

df = load_data()

# Show raw data
st.subheader("🔍 Dataset Preview")
st.dataframe(df, use_container_width=True)

# Sidebar filters
st.sidebar.header("Filters")

numeric_cols = df.select_dtypes(include=["int64", "float64"]).columns.tolist()
cat_cols = df.select_dtypes(include=["object"]).columns.tolist()

if cat_cols:
    selected_col = st.sidebar.selectbox("Select Category Column", cat_cols)
    selected_val = st.sidebar.multiselect(
        "Select Values",
        df[selected_col].dropna().unique()
    )

    if selected_val:
        df = df[df[selected_col].isin(selected_val)]

# KPIs
st.subheader("📌 Summary Statistics")
st.write(df.describe())

# Charts
st.subheader("📈 Visualizations")

if numeric_cols:
    col1, col2 = st.columns(2)

    with col1:
        x_axis = st.selectbox("X Axis", df.columns)
    with col2:
        y_axis = st.selectbox("Y Axis", numeric_cols)

    fig, ax = plt.subplots()
    ax.plot(df[x_axis], df[y_axis], marker="o")
    ax.set_xlabel(x_axis)
    ax.set_ylabel(y_axis)
    ax.set_title(f"{y_axis} vs {x_axis}")
    plt.xticks(rotation=45)

    st.pyplot(fig)

# Footer
st.markdown("---")
st.markdown("Built with ❤️ using Streamlit")
