import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Load your Excel file
df = pd.read_excel("Time off Report.xlsx")

# Clean column names (remove extra spaces)
df.columns = df.columns.str.strip()

# Show column names in the app (for debugging)
st.write("Colonnes détectées :", df.columns.tolist())

# Calculate difference between Factorial Available and Contract Available
df["Difference"] = df["Available"] - df["Solde Contrat"]

# Segment employees into groups
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
sns.histplot(df["Difference"], bins=20, kde=True, ax=ax1)
ax1.set_xlabel("Écart (Factorial - Contrat)")
ax1.set_ylabel("Nombre d'employés")
st.pyplot(fig1)

# --- 3. Scatter plot ---
st.subheader("Comparaison des soldes : Contrat vs Factorial")
fig2, ax2 = plt.subplots()
sns.scatterplot(x=df["Solde Contrat"], y=df["Available"], hue=df["Group"], ax=ax2)
ax2.plot([df["Solde Contrat"].min(), df["Solde Contrat"].max()],
         [df["Solde Contrat"].min(), df["Solde Contrat"].max()],
         'r--')  # diagonal line
ax2.set_xlabel("Solde Contrat")
ax2.set_ylabel("Solde Factorial")
st.pyplot(fig2)

# --- 4. Top anomalies ---
st.subheader("Top 10 écarts positifs (Factorial > Contrat)")
st.dataframe(df.nlargest(10, "Difference")[["NOM", "Prénom", "Solde Contrat", "Available", "Difference"]])

st.subheader("Top 10 écarts négatifs (Contrat > Factorial)")
st.dataframe(df.nsmallest(10, "Difference")[["NOM", "Prénom", "Solde Contrat", "Available", "Difference"]])
