import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="🏆 DZMatch Votes", layout="wide")
st.title("🏆 DZMatch Votes")

# 🔹 Fichier local pour enregistrer les votes
FILE_VOTES = "votes.xlsx"

# 🔹 Barème des points
points = {1:5, 2:3, 3:2, 4:1, 5:0.5}

# 🔹 Catégories et participants
categories = {
    "Meilleur gardien": [
        "Oussama Benbout (USMA)", "Zakaria Bouhalfaya (CSC)", "Abderrahmane Medjadel (ASO)",
        "Tarek Boussder (ESS)", "Abdelkader Salhi (MCEB)", "Zeghba (CRB)",
        "Hadid (JSK)", "Ramdane (MCA)"
    ],
    "Meilleur club": ["MCA", "USMA", "CSC", "CRB", "JSK", "PAC", "ESS"],
    "Meilleur joueur": [
        "Adel Boulbina (PAC)", "Aymen Mahious (CRB)", "Abderrahmane Meziane (CRB)",
        "Ibrahim Dib (CSC)", "Salim Boukhenchouch (USMA)", "Larbi Tabti (MCA)",
        "Mehdi Boudjamaa (JSK)"
    ],
    "Meilleur entraîneur": [
        "Khaled Benyahia (MCA)", "Joseph Zinbauer (JSK)", "Sead Ramovic (CRB)",
        "Khereddine Madoui (CSC)", "Bilal Dziri (PAC)"
    ]
}

# 🔹 Saisie des votes
st.write("Votez pour vos favoris dans chaque catégorie (TOP 5 par ordre).")
nom_votant = st.text_input("📝 Entrez votre nom et prénom :")
vote_data = {}

with st.form("vote_form"):
    for cat, participants in categories.items():
        st.subheader(cat)
        top5 = st.multiselect(
            f"Sélectionnez votre TOP 5 pour {cat} (ordre important)",
            options=participants,
            max_selections=5,
            key=cat
        )
        vote_data[cat] = top5
    submitted = st.form_submit_button("✅ Envoyer mon vote")

# 🔹 Fonction pour sauvegarder le vote
def save_vote(nom, votes):
    if os.path.exists(FILE_VOTES):
        df = pd.read_excel(FILE_VOTES)
    else:
        df = pd.DataFrame(columns=["Nom", "Categorie", "Candidat", "Position", "Points"])

    if nom in df["Nom"].values:
        return False  # déjà voté

    for cat, top5 in votes.items():
        for i, candidat in enumerate(top5, start=1):
            point = points.get(i, 0)
            df = pd.concat([df, pd.DataFrame([[nom, cat, candidat, i, point]], columns=df.columns)])
    
    df.to_excel(FILE_VOTES, index=False)
    return True

# 🔹 Traitement du vote
if submitted:
    if not nom_votant.strip():
        st.error("⚠️ Vous devez entrer votre nom et prénom avant de voter.")
    else:
        success = save_vote(nom_votant, vote_data)
        if success:
            st.success(f"Merci {nom_votant}, votre vote a été enregistré ! 🎉")
        else:
            st.error("⚠️ Vous avez déjà voté.")

# 🔹 Affichage des résultats en temps réel
st.header("📊 Classements en temps réel")
if os.path.exists(FILE_VOTES):
    df = pd.read_excel(FILE_VOTES)
    for cat in categories:
        st.subheader(cat)
        df_cat = df[df["Categorie"] == cat].groupby("Candidat")["Points"].sum().reset_index()
        if not df_cat.empty:
            df_cat = df_cat.sort_values(by="Points", ascending=False)
            df_cat.insert(0, "Position", range(1, len(df_cat)+1))
            st.dataframe(df_cat, use_container_width=True)
        else:
            st.info("Aucun vote pour cette catégorie.")
else:
    st.info("Aucun vote enregistré pour le moment.")
