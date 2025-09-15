import streamlit as st
import pandas as pd

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
    "Meilleur club": [
        "MCA", "USMA", "CSC", "CRB", "JSK", "PAC", "ESS"
    ],
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
# Stockage global (mémoire de session)
# -------------------------------
if "votes" not in st.session_state:
    st.session_state.votes = {cat: {} for cat in categories}
if "votants" not in st.session_state:
    st.session_state.votants = set()  # pour stocker les noms des votants

# -------------------------------
# Fonction pour enregistrer un vote
# -------------------------------
def ajouter_vote(categorie, top5):
    for i, candidat in enumerate(top5, start=1):
        score = points.get(i, 0)
        st.session_state.votes[categorie][candidat] = (
            st.session_state.votes[categorie].get(candidat, 0) + score
        )

# -------------------------------
# Interface Streamlit
# -------------------------------
st.title("🏆 Système de vote championnat")

st.write("Votez pour vos favoris dans chaque catégorie (TOP 5).")

# Nom du votant
nom_votant = st.text_input("📝 Entrez votre nom et prénom :")

vote_data = {}

# Formulaire de vote
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
# Traitement du vote
# -------------------------------
if submitted:
    if not nom_votant.strip():
        st.error("⚠️ Vous devez entrer votre nom et prénom avant de voter.")
    elif nom_votant in st.session_state.votants:
        st.error("⚠️ Vous avez déjà voté, un seul vote est autorisé.")
    else:
        for cat, top5 in vote_data.items():
            ajouter_vote(cat, top5)
        st.session_state.votants.add(nom_votant)
        st.success(f"Merci {nom_votant}, votre vote a été enregistré avec succès ! 🎉")

# -------------------------------
# Affichage des résultats en temps réel
# -------------------------------
st.header("📊 Classements en temps réel")

for cat in categories:
    st.subheader(cat)
    classement = sorted(
        st.session_state.votes[cat].items(),
        key=lambda x: x[1],
        reverse=True
    )
    if classement:
        # Créer DataFrame avec Position, Candidat, Points
        df = pd.DataFrame(classement, columns=["Candidat", "Points"])
        df.insert(0, "Position", range(1, len(df) + 1))

        # Afficher sans l’index automatique
        st.dataframe(df, use_container_width=True, hide_index=True)
    else:
        st.info("Aucun vote enregistré pour cette catégorie.")
