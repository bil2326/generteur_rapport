import streamlit as st
import os
import tempfile
from datetime import date
from report import Report


def update_backend_report_content(etat, diag, preco):
    st.session_state.report.content["etat_des_lieux"] = []
    for element in etat.split("\n"):
        st.session_state.report.content["etat_des_lieux"].append(element[2:])
       
    st.session_state.report.content["diagnostic"] = []
    for element in diag.split("\n"):
        st.session_state.report.content["diagnostic"].append(element[2:])
    
    st.session_state.report.content["preconisation"] = []
    for element in preco.split("\n"):
        st.session_state.report.content["preconisation"].append(element[2:])


st.set_page_config(layout="wide")
st.title("📝 Générateur de rapports DOCX")

if "report" not in st.session_state:
    st.session_state.report = None

# --- SECTION 1: Introduction ---
st.header("Introduction")

with st.form("intro_form"):
    report_id = st.number_input("Numéro du rapport (DE / ETUDE-01809)", step=1, format="%d")
    subject = st.text_input("Sujet du rapport")
    intervention_date = st.date_input("Date d'intervention", value=date.today())
    zone = st.text_input("Zone d'intervention")
    site = st.text_input("Site")

    submitted = st.form_submit_button("Initialiser le rapport")
    if submitted:
        st.session_state.report = Report(
            report_id, subject, str(intervention_date), zone, site
        )
        st.success("Rapport initialisé")

# --- SECTION 2-4: Upload + Génération ---
if st.session_state.report:
    st.header("✍️ Rédaction assistée des sections : Constat, Diagnostic, Préconisations")
    image_file = st.file_uploader("Image", type=["jpg", "jpeg", "png"])
    audio_file = st.file_uploader("Fichier vocal", type=["mp3", "wav", "m4a"])

    if st.button("Ajouter au rapport"):
        if image_file and audio_file:
            img_path = os.path.join(tempfile.gettempdir(), image_file.name)
            audio_path = os.path.join(tempfile.gettempdir(), audio_file.name)
            with open(img_path, "wb") as f:
                f.write(image_file.read())
            with open(audio_path, "wb") as f:
                f.write(audio_file.read())
            st.session_state.report.add_image(img_path)
            st.session_state.report.add_vocal(audio_path)
            st.success("Médias ajoutés")
            st.session_state.report.write_content(img_path, audio_path)
        else:
            st.warning("Ajoutez une image et un vocal")


        
        st.success("Contenu généré ! Vous pouvez le modifier ci-dessous")

    # --- Affichage et édition ---
    st.subheader("🧾 Contenu généré")
    etat = st.text_area("État des lieux", value=f'+ {"\n+ ".join(st.session_state.report.content["etat_des_lieux"])}')
    diag = st.text_area("Diagnostic", value=f'+ {"\n+ ".join(st.session_state.report.content["diagnostic"])}')
    preco = st.text_area("Préconisations", value=f'+ {"\n+ ".join(st.session_state.report.content["preconisation"])}')

    if st.button("Mettre à jour le contenu"):
        update_backend_report_content(etat, diag, preco)
        print(st.session_state.report)
        st.success("Modification manuelle prise en compte")

    # --- Export ---
    if st.button("📁 Exporter en DOCX"):
        docx_path = os.path.join(tempfile.gettempdir(), "rapport_final.docx")
        st.session_state.report.export_report_as_docx_file(docx_path)
        with open(docx_path, "rb") as f:
            st.download_button("Télécharger le rapport", f, file_name="rapport.docx")

