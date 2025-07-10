import streamlit as st
import os
import tempfile
import uuid
from datetime import date
from utils_drive import GoogleDriveManager

from report import Report



from dotenv import load_dotenv
drive_manager = GoogleDriveManager()
load_dotenv()



dict_file_name_id = drive_manager.gets_files_names_and_ids(dossier_id=os.environ["ID_CTICM_DIRECTORY"])

# Affichage du chargement d'un ancien projet que si mémoire il ya
if dict_file_name_id.keys():
    st.title("Charger un ancien projet")
    selection = st.selectbox(
        "Choisissez une option :",
        list(dict_file_name_id.keys()),
        index=0  # Index de l'option sélectionnée par défaut (0 = première option)
    )



    if st.button("Charger le projet", type="primary"):
        with st.spinner("Traitement en cours..."):
            st.session_state.report = drive_manager.load_report(fichier_id=dict_file_name_id[selection])
            st.write(f"Vous venez de charger : **{st.session_state.report.report_id}**")



def update_backend_report_content(etat, diag, preco):
    """Met à jour l'objet Report en backend après édition manuelle."""
    st.session_state.report.content["etat_des_lieux"] = [e[2:] for e in etat.split("\n") if e.strip()]
    st.session_state.report.content["diagnostic"] = [d[2:] for d in diag.split("\n") if d.strip()]
    st.session_state.report.content["preconisation"] = [p[2:] for p in preco.split("\n") if p.strip()]


st.set_page_config(layout="wide")
st.title("📝 Générateur de rapports DOCX")



# --- SECTION 1: Introduction ---
st.header("Introduction")
# Charger un ancien rapport
if "report" in st.session_state:
    report_id = st.write(f"**Identifiant du rapport : {st.session_state.report.report_id}**")
    subject = st.write(f"**Sujet du rapport : {st.session_state.report.report_subject}**")
    intervention_date = st.write(f"**Date d'intervention : {st.session_state.report.intervention_date}**")
    zone = st.write(f"**Zone d'intervention : {st.session_state.report.intervention_zone}**")
    site = st.write(f"**Site d'intervention : {st.session_state.report.site}**")

#initialiser un nouveau rapport  
else:
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
        st.success("Rapport initialisé ✅")





# --- SECTION 2‑4: Upload + Génération ---
if "report" in st.session_state:
    st.header("✍️ Rédaction assistée – Constat / Diagnostic / Préconisations")
    if st.session_state.report.images:
        for image_bytes in st.session_state.report.images:
            st.image(image_bytes)

    image_file = st.file_uploader("Image (jpg, png)", type=["jpg", "jpeg", "png"])
    if image_file:
        image_bytes = image_file.read()
        st.image(image_bytes)

    # 🎤 Nouveau widget : enregistrement vocal push‑to‑talk
    audio_data = st.audio_input("🎤 Maintenez pour enregistrer le vocal")

    # Construire le rapport lorsque les deux médias sont disponibles
    if st.button("Ajouter au rapport"):
        if image_file is not None and audio_data is not None:


            # Sauvegarde de l'audio enregistré dans un fichier WAV unique
            audio_filename = f"{uuid.uuid4()}.wav"
            audio_path = os.path.join(tempfile.gettempdir(), audio_filename)
            with open(audio_path, "wb") as f_audio:
                f_audio.write(audio_data.read())

            # Injection dans l'objet Report

            # Génération du contenu par les API Mistral + Whisper
            with st.spinner("Analyse en cours…"):
                st.session_state.report.write_content(image_bytes, audio_path)
                st.session_state.report.add_image(image_bytes)
                st.session_state.report.add_vocal(audio_path)

            st.success("Médias ajoutés et contenu généré !")
        else:
            st.warning("Veuillez fournir **une image** et **un enregistrement vocal** avant de continuer.")

    # --- Affichage et édition ---
    if st.session_state.report.content["etat_des_lieux"]:
        st.subheader("🧾 Contenu généré")
        etat = st.text_area(
            "État des lieux",
            value='+ ' + "\n+ ".join(st.session_state.report.content["etat_des_lieux"]),
            height=200,
        )
        diag = st.text_area(
            "Diagnostic",
            value='+ ' + "\n+ ".join(st.session_state.report.content["diagnostic"]),
            height=200,
        )
        preco = st.text_area(
            "Préconisations",
            value='+ ' + "\n+ ".join(st.session_state.report.content["preconisation"]),
            height=200,
        )

        if st.button("Mettre à jour le contenu"):
            update_backend_report_content(etat, diag, preco)
            st.success("Contenu mis à jour ✔️")

        # --- Exportation DOCX ---
        if st.button("📁 Sauvegarder le rapport sur le drive"):
            drive_manager.uploader_report(report_object=st.session_state.report,\
                               nom_fichier=st.session_state.report.report_id,\
                               dossier_id=os.environ["ID_CTICM_DIRECTORY"])

        docx_path = os.path.join(tempfile.gettempdir(), "rapport_final.docx")
        st.session_state.report.export_report_as_docx_file(docx_path)
        with open(docx_path, "rb") as f:
            st.download_button("📁 Télécharger le rapport", f, file_name="rapport.docx")
