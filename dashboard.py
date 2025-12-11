import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Load Excel file and skip first row to reach actual headers
df = pd.read_excel("Time off Report.xlsx", header=1)

# Clean column names
df.columns = df.columns.str.strip()

# Show column names for debugging
st.write("Colonnes détectées :", df.columns.tolist())

# Check if required columns exist
required_cols = ["Solde Contrat", "Available", "NOM", "Prénom"]
missing = [col for col in required_cols if col not in df.columns]
if missing:
    st.error(f"Colonnes manquantes : {missing}")
else:
    # Convert to numeric to avoid plotting errors
    df["Solde Contrat"] = pd.to_numeric(df["Solde Contrat"], errors="coerce")
    df["Available"] = pd.to_numeric(df["Available"], errors="coerce")

    # Calculate difference
    df["Difference"] = df["Available"] - df["Solde Contrat"]

    # Segment employees
    df["Group"] = df["Difference"].apply(
        lambda x: "Factorial > Contract" if x > 0 else ("Contract > Factorial" if x < 0 else "Aligned")
    )

    st.title("Holiday Balance Dashboard")

    # --- 1. Bar chart of groups ---
    st.subheader("Répartition des employés par anomalie")
    st.bar_chart(df["Group"].value_counts())

    # --- 2. Histogram of differences ---
    st.subheader("Distribution des écarts (jours)")
    fig1, ax1 = plt.subplots()
    sns.histplot(df["Difference"].dropna(), bins=20, kde=True, ax=ax1)
    ax1.set_xlabel("Écart (Factorial - Contrat)")
    ax1.set_ylabel("Nombre d'employés")
    st.pyplot(fig1)

    # --- 3. Scatter plot ---
    st.subheader("Comparaison des soldes : Contrat vs Factorial")
    df_clean = df.dropna(subset=["Solde Contrat", "Available", "Group"])
    fig2, ax2 = plt.subplots()
    sns.scatterplot(x=df_clean["Solde Contrat"], y=df_clean["Available"], hue=df_clean["Group"], ax=ax2)
    ax2.plot([df_clean["Solde Contrat"].min(), df_clean["Solde Contrat"].max()],
             [df_clean["Solde Contrat"].min(), df_clean["Solde Contrat"].max()],
             'r--')
    ax2.set_xlabel("Solde Contrat")
    ax2.set_ylabel("Solde Factorial")
    st.pyplot(fig2)

    # --- 4. Top anomalies ---
    st.subheader("Top 10 écarts positifs (Factorial > Contrat)")
    st.dataframe(df.nlargest(10, "Difference")[["NOM", "Prénom", "Solde Contrat", "Available", "Difference"]])

    st.subheader("Top 10 écarts négatifs (Contrat > Factorial)")
    st.dataframe(df.nsmallest(10, "Difference")[["NOM", "Prénom", "Solde Contrat", "Available", "Difference"]])
