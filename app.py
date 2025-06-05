import streamlit as st
import os
import tempfile
import uuid
from datetime import date
from report import Report


def update_backend_report_content(etat, diag, preco):
    """Met à jour l'objet Report en backend après édition manuelle."""
    st.session_state.report.content["etat_des_lieux"] = [e[2:] for e in etat.split("\n") if e.strip()]
    st.session_state.report.content["diagnostic"] = [d[2:] for d in diag.split("\n") if d.strip()]
    st.session_state.report.content["preconisation"] = [p[2:] for p in preco.split("\n") if p.strip()]


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
        st.success("Rapport initialisé ✅")

# --- SECTION 2‑4: Upload + Génération ---
if st.session_state.report:
    st.header("✍️ Rédaction assistée – Constat / Diagnostic / Préconisations")

    # Image upload (inchangé)
    image_file = st.file_uploader("Image (jpg, png)", type=["jpg", "jpeg", "png"])

    # 🎤 Nouveau widget : enregistrement vocal push‑to‑talk
    audio_data = st.audio_input("🎤 Maintenez pour enregistrer le vocal")

    # Construire le rapport lorsque les deux médias sont disponibles
    if st.button("Ajouter au rapport"):
        if image_file is not None and audio_data is not None:
            # Sauvegarde de l'image sur le disque temporaire
            img_path = os.path.join(tempfile.gettempdir(), image_file.name)
            with open(img_path, "wb") as f_img:
                f_img.write(image_file.read())

            # Sauvegarde de l'audio enregistré dans un fichier WAV unique
            audio_filename = f"{uuid.uuid4()}.wav"
            audio_path = os.path.join(tempfile.gettempdir(), audio_filename)
            with open(audio_path, "wb") as f_audio:
                f_audio.write(audio_data.read())

            # Injection dans l'objet Report
            st.session_state.report.add_image(img_path)
            st.session_state.report.add_vocal(audio_path)

            # Génération du contenu par les API Mistral + Whisper
            with st.spinner("Analyse en cours…"):
                st.session_state.report.write_content(img_path, audio_path)

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
        if st.button("📁 Exporter en DOCX"):
            docx_path = os.path.join(tempfile.gettempdir(), "rapport_final.docx")
            st.session_state.report.export_report_as_docx_file(docx_path)
            with open(docx_path, "rb") as f:
                st.download_button("Télécharger le rapport", f, file_name="rapport.docx")
