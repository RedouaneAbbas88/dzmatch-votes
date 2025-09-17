import streamlit as st
import pandas as pd
import os

st.title("🏆 DZMatch Votes")

# Fichier local pour enregistrer les votes
FILE_VOTES = "votes.xlsx"

# Barème des points
points = {1:5, 2:3, 3:2, 4:1, 5:0.5}

# Catégories et participants
categories = {
    "Meilleur gardien": ["Oussama", "Zakaria", "Abderrahmane", "Tarek", "Abdelkader"],
    "Meilleur club": ["MCA", "USMA", "CSC", "CRB", "JSK"],
    "Meilleur joueur": ["Adel", "Aymen", "Mehdi", "Larbi", "Salim"]
}

# Saisie des votes
nom_votant = st.text_input("📝 Entrez votre nom :")
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

# Fonction pour sauvegarder
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

# Traitement
if submitted:
    if not nom_votant.strip():
        st.error("⚠️ Entrez votre nom.")
    else:
        success = save_vote(nom_votant, vote_data)
        if success:
            st.success(f"Merci {nom_votant}, votre vote a été enregistré ! 🎉")
        else:
            st.error("⚠️ Vous avez déjà voté.")

# Affichage des résultats
st.header("📊 Classements en temps réel")
if os.path.exists(FILE_VOTES):
    df = pd.read_excel(FILE_VOTES)
    for cat in categories:
        st.subheader(cat)
        df_cat = df[df["Categorie"]==cat].groupby("Candidat")["Points"].sum().reset_index()
        df_cat = df_cat.sort_values(by="Points", ascending=False)
        st.dataframe(df_cat)
else:
    st.info("Aucun vote enregistré pour le moment.")
