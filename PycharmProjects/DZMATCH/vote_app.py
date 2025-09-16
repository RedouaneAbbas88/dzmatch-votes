import streamlit as st
import gspread
import pandas as pd
from google.oauth2.service_account import Credentials
import json

# -------------------------------
# Connexion à Google Sheets
# -------------------------------
SPREADSHEET_ID = st.secrets["google"]["SPREADSHEET_ID"]

# Lire les credentials depuis le secret
creds_dict = json.loads(st.secrets["google"]["GOOGLE_CREDS_JSON"])
creds = Credentials.from_service_account_info(
    creds_dict,
    scopes=["https://www.googleapis.com/auth/spreadsheets"]
)

gc = gspread.authorize(creds)
sheet = gc.open_by_key(SPREADSHEET_ID).sheet1

# -------------------------------
# Barème des points
# -------------------------------
points = {1: 5, 2: 3, 3: 2, 4: 1, 5: 0.5}

# -------------------------------
# Participants par catégorie
# -------------------------------
categories = {
    "Meilleur gardien": [
        "Oussama Benbout (USMA)",
        "Zakaria Bouhalfaya (CSC)",
        "Abderrahmane Medjadel (ASO)",
        "Tarek Boussder (ESS)",
        "Abdelkader Salhi (MCEB)",
        "Zeghba (CRB)",
        "Hadid (JSK)",
        "Ramdane (MCA)"
    ],
    "Meilleur club": ["MCA", "USMA", "CSC", "CRB", "JSK", "PAC", "ESS"],
    "Meilleur joueur": [
        "Adel Boulbina (PAC)",
        "Aymen Mahious (CRB)",
        "Abderrahmane Meziane (CRB)",
        "Ibrahim Dib (CSC)",
        "Salim Boukhenchouch (USMA)",
        "Larbi Tabti (MCA)",
        "Mehdi Boudjamaa (JSK)"
    ],
    "Meilleur entraîneur": [
        "Khaled Benyahia (MCA)",
        "Joseph Zinbauer (JSK)",
        "Sead Ramovic (CRB)",
        "Khereddine Madoui (CSC)",
        "Bilal Dziri (PAC)"
    ]
}

# -------------------------------
# Interface Streamlit
# -------------------------------
st.title("🏆 Système de vote championnat")
st.write("Votez pour vos favoris dans chaque catégorie (TOP 5).")

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

# -------------------------------
# Fonction pour sauvegarder le vote dans Google Sheet
# -------------------------------
def save_vote(nom, votes):
    try:
        data = sheet.get_all_records()
        df = pd.DataFrame(data)
    except:
        df = pd.DataFrame(columns=["Nom", "Categorie", "Candidat", "Position", "Points"])

    # Vérifier si le votant a déjà voté
    if not df.empty and nom in df["Nom"].values:
        return False

    # Ajouter les votes
    for cat, top5 in votes.items():
        for i, candidat in enumerate(top5, start=1):
            point = points.get(i, 0)
            sheet.append_row([nom, cat, candidat, i, point])
    return True

# -------------------------------
# Traitement du vote
# -------------------------------
if submitted:
    if not nom_votant.strip():
        st.error("⚠️ Vous devez entrer votre nom et prénom avant de voter.")
    else:
        success = save_vote(nom_votant, vote_data)
        if success:
            st.success(f"Merci {nom_votant}, votre vote a été enregistré ! 🎉")
        else:
            st.error("⚠️ Vous avez déjà voté.")

# -------------------------------
# Affichage des résultats en temps réel
# -------------------------------
st.header("📊 Classements en temps réel")
try:
    data = sheet.get_all_records()
    df = pd.DataFrame(data)
    for cat in categories:
        st.subheader(cat)
        if cat in df["Categorie"].values:
            df_cat = df[df["Categorie"] == cat].groupby("Candidat")["Points"].sum().reset_index()
            df_cat = df_cat.sort_values(by="Points", ascending=False)
            df_cat.insert(0, "Position", range(1, len(df_cat)+1))
            st.dataframe(df_cat, use_container_width=True)
        else:
            st.info("Aucun vote pour cette catégorie.")
except Exception:
    st.info("Aucun vote enregistré pour le moment.")
