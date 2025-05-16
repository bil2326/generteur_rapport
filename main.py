import streamlit as st
import datetime
from Backend import init_doc, generateur_introduction, get_buffer  # Importation de la fonction

st.set_page_config(page_title="Générateur de Rapport", layout="centered")

st.subheader("🧩 I) Introduction")

# Champs du formulaire
sujet = st.text_input("📌 Sujet du rapport")

date_intervention = st.date_input("📅 Date d'intervention", value=datetime.date.today())

zone = st.text_area("🌍 Zone d’intervention")

site = st.text_area("🏗️ Site")

# Bouton pour générer
if st.button("📄 Générer le rapport"):
    if not sujet or not zone or not site:
        st.warning("Veuillez remplir tous les champs avant de générer le rapport.")
    else:
        doc = init_doc()
        doc = generateur_introduction(doc, sujet, date_intervention, zone, site)
        buffer = get_buffer(doc)

        st.success("✅ Rapport généré avec succès !")

        st.download_button(
            label="📥 Télécharger le rapport Word",
            data=buffer,
            file_name="rapport.docx",
            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        )
