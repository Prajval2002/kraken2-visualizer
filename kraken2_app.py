import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(page_title="Kraken2 Report Visualizer", layout="wide")

st.title("🦠 Kraken2 Report Visualizer")
st.markdown("Upload your Kraken2 `.report` file to view taxonomic composition.")

uploaded_file = st.file_uploader("Upload Kraken2 report file", type=["report", "txt"])

if uploaded_file is not None:
    # Read the Kraken2 report into a DataFrame
    df = pd.read_csv(uploaded_file, sep='\t', header=None, names=[
        "percent", "reads", "reads_direct", "rank", "ncbi_taxid", "name"
    ])
    
    # Basic stats
    st.subheader("📊 Summary Stats")
    st.write(df.describe())
    
    # Top N taxa by abundance
    st.subheader("🔬 Top Taxa by Abundance")
    top_n = st.slider("Select Top N Taxa", min_value=5, max_value=50, value=10)
    top_taxa = df.sort_values("percent", ascending=False).head(top_n)

    # Bar plot
    fig, ax = plt.subplots(figsize=(10, 5))
    sns.barplot(data=top_taxa, x="percent", y="name", ax=ax)
    ax.set_xlabel("Percent of Reads")
    ax.set_ylabel("Taxonomic Name")
    st.pyplot(fig)

    # Show raw Kraken report
    st.subheader("📄 Raw Kraken Report (preview)")
    st.dataframe(df.head(20))
