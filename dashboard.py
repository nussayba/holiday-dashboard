import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Charger le fichier
df = pd.read_excel("Time off Report.xlsx", header=1)
df.columns = df.columns.str.strip()

# Vérifier les colonnes nécessaires
required = [
    "Accrued Factorial", "Taken", "Available",
    "Accrued", "Taken.1", "Available.1",
    "Solde Contrat", "NOM", "Prénom"
]
missing = [col for col in required if col not in df.columns]
if missing:
    st.error(f"Colonnes manquantes : {missing}")
else:
    # Renommer pour clarté
    df = df.rename(columns={
        "Accrued Factorial": "Accrued_2024",
        "Taken": "Taken_2024",
        "Available": "Available_2024",
        "Accrued": "Accrued_2025",
        "Taken.1": "Taken_2025",
        "Available.1": "Available_2025"
    })

    # Conversion en numérique
    numeric_cols = [
        "Accrued_2024", "Taken_2024", "Available_2024",
        "Accrued_2025", "Taken_2025", "Available_2025",
        "Solde Contrat"
    ]
    for col in numeric_cols:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    # ----------------------------------------------------------------------
    # ✅ 1. Comparaison Solde Contrat vs Accrued 2024
    # ----------------------------------------------------------------------
    df["Delta_Contrat"] = df["Accrued_2024"] - df["Solde Contrat"]
    df["Contrat_Status"] = df["Delta_Contrat"].apply(
        lambda x: "Accrued > Contrat" if x > 0 else ("Accrued < Contrat" if x < 0 else "Aligné")
    )

    st.title("Audit RH – Comparaison Solde Contrat vs Accrued 2024")

    st.subheader("Répartition des écarts")
    st.bar_chart(df["Contrat_Status"].value_counts())

    st.subheader("Distribution des écarts (Accrued_2024 - Solde Contrat)")
    fig0, ax0 = plt.subplots()
    sns.histplot(df["Delta_Contrat"].dropna(), bins=20, kde=True, ax=ax0)
    ax0.set_xlabel("Écart en jours")
    ax0.set_ylabel("Nombre d'employés")
    st.pyplot(fig0)

    st.subheader("Écarts triés du plus grand au plus petit")
    st.dataframe(
        df.sort_values("Delta_Contrat", ascending=False)[
            ["NOM", "Prénom", "Accrued_2024", "Solde Contrat", "Delta_Contrat"]
        ]
    )

    st.subheader("Écarts triés du plus petit au plus grand")
    st.dataframe(
        df.sort_values("Delta_Contrat", ascending=True)[
            ["NOM", "Prénom", "Accrued_2024", "Solde Contrat", "Delta_Contrat"]
        ]
    )

    # ----------------------------------------------------------------------
    # ✅ 2. Audit interne Factorial 2024 & 2025
    # ----------------------------------------------------------------------
    df["Delta_2024"] = df["Accrued_2024"] - (df["Taken_2024"] + df["Available_2024"])
    df["Delta_2025"] = df["Accrued_2025"] - (df["Taken_2025"] + df["Available_2025"])

    df["Status_2024"] = df["Delta_2024"].apply(
        lambda x: "Aligné" if abs(x) < 0.01 else ("Excès" if x > 0 else "Déficit")
    )
    df["Status_2025"] = df["Delta_2025"].apply(
        lambda x: "Aligné" if abs(x) < 0.01 else ("Excès" if x > 0 else "Déficit")
    )

    year = st.selectbox("Choisir l'année à analyser", ["2024", "2025"])

    st.title(f"Audit interne Factorial – {year}")

    if year == "2024":
        st.subheader("Répartition des écarts internes")
        st.bar_chart(df["Status_2024"].value_counts())

        st.subheader("Distribution des écarts (Accrued - [Taken + Available])")
        fig1, ax1 = plt.subplots()
        sns.histplot(df["Delta_2024"].dropna(), bins=20, kde=True, ax=ax1)
        ax1.set_xlabel("Écart en jours")
        ax1.set_ylabel("Nombre d'employés")
        st.pyplot(fig1)

        st.subheader("Écarts 2024 triés du plus grand au plus petit")
        st.dataframe(
            df.sort_values("Delta_2024", ascending=False)[
                ["NOM", "Prénom", "Accrued_2024", "Taken_2024", "Available_2024", "Delta_2024"]
            ]
        )

        st.subheader("Écarts 2024 triés du plus petit au plus grand")
        st.dataframe(
            df.sort_values("Delta_2024", ascending=True)[
                ["NOM", "Prénom", "Accrued_2024", "Taken_2024", "Available_2024", "Delta_2024"]
            ]
        )

    else:
        st.subheader("Répartition des écarts internes")
        st.bar_chart(df["Status_2025"].value_counts())

        st.subheader("Distribution des écarts (Accrued - [Taken + Available])")
        fig2, ax2 = plt.subplots()
        sns.histplot(df["Delta_2025"].dropna(), bins=20, kde=True, ax=ax2)
        ax2.set_xlabel("Écart en jours")
        ax2.set_ylabel("Nombre d'employés")
        st.pyplot(fig2)

        st.subheader("Écarts 2025 triés du plus grand au plus petit")
        st.dataframe(
            df.sort_values("Delta_2025", ascending=False)[
                ["NOM", "Prénom", "Accrued_2025", "Taken_2025", "Available_2025", "Delta_2025"]
            ]
        )

        st.subheader("Écarts 2025 triés du plus petit au plus grand")
        st.dataframe(
            df.sort_values("Delta_2025", ascending=True)[
                ["NOM", "Prénom", "Accrued_2025", "Taken_2025", "Available_2025", "Delta_2025"]
            ]
        )
