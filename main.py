import streamlit as st
import datetime
from doc_writer import *
from ai_agent import *
from PIL import Image

st.set_page_config(page_title="Générateur de Rapport", layout="centered")

st.subheader("I) Introduction")
sujet = st.text_input("📌 Sujet du rapport")
date_intervention = st.date_input("📅 Date d'intervention", value=datetime.date.today())
zone = st.text_area("🌍 Zone d’intervention")
site = st.text_area("🏗️ Site")







st.subheader("II) état des lieux/Constat")
st.write("Veuillez introduire l'image et les mots clefs pour guider l'IA .")
user_input_2_section = st.text_input("Indiquez des mots clefs")
uploaded_file = st.file_uploader(
    "Prends ou choisis une photo", 
    type=["jpg", "jpeg", "png"]
)

if uploaded_file and st.button("Valider l'étape 2"):
    image = Image.open(uploaded_file)
    constat = build_constat(image, user_input_2_section)
    st.image(image, caption="Image importée", use_container_width=True)
    st.write(constat)









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
