import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Load your Excel file
df = pd.read_excel("Time off Report.xlsx")

# Calculate difference between Factorial Available and Contract Available
df["Difference"] = df["Available"] - df["Solde Contrat"]

# Segment employees into groups
df["Group"] = df["Difference"].apply(
    lambda x: "Factorial > Contract" if x > 0 else ("Contract > Factorial" if x < 0 else "Aligned")
)

st.title("Holiday Balance Dashboard")

# --- 1. Bar chart of groups ---
st.subheader("Employee Segmentation")
st.bar_chart(df["Group"].value_counts())

# --- 2. Histogram of differences ---
st.subheader("Distribution of Differences")
fig1, ax1 = plt.subplots()
sns.histplot(df["Difference"], bins=20, kde=True, ax=ax1)
ax1.set_xlabel("Difference (Factorial - Contract)")
ax1.set_ylabel("Count")
st.pyplot(fig1)

# --- 3. Scatter plot ---
st.subheader("Contract vs Factorial Balances")
fig2, ax2 = plt.subplots()
sns.scatterplot(x=df["Solde Contrat"], y=df["Available"], hue=df["Group"], ax=ax2)
ax2.plot([df["Solde Contrat"].min(), df["Solde Contrat"].max()],
         [df["Solde Contrat"].min(), df["Solde Contrat"].max()],
         'r--')  # diagonal line
ax2.set_xlabel("Contract Available")
ax2.set_ylabel("Factorial Available")
st.pyplot(fig2)

# --- 4. Top anomalies ---
st.subheader("Top 10 Positive Differences (Factorial > Contract)")
st.dataframe(df.nlargest(10, "Difference")[["NOM", "Prénom", "Solde Contrat", "Available", "Difference"]])

st.subheader("Top 10 Negative Differences (Contract > Factorial)")
st.dataframe(df.nsmallest(10, "Difference")[["NOM", "Prénom", "Solde Contrat", "Available", "Difference"]])
