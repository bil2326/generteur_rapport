import pickle
from docx import Document
from datetime import datetime
from api_calls import build_content

class Report:
    def __init__(self, report_id, report_subject, intervention_date, intervention_zone, site):
        self.report_id = f"DE / ETUDE-01809 / {report_id}"
        self.report_subject = report_subject
        self.intervention_date = intervention_date
        self.intervention_zone = intervention_zone
        self.site = site
        self.content = {
            "etat_des_lieux": [],
            "diagnostic": [],
            "preconisation": []
        }
        self.images = []
        self.vocals = []


    def add_image(self, image_path):
        self.images.append(image_path)

    def add_vocal(self, vocal_path):
        self.vocals.append(vocal_path)

    def write_content(self, image_path, vocal_path):

        section_result = build_content(image_path, vocal_path)
        # parse result json string if needed
        self.content["etat_des_lieux"].append(section_result["etat_des_lieux"])
        self.content["diagnostic"].append(section_result["diagnostic"])
        self.content["preconisation"].append(section_result["preconisation"])

    def save_as_pkl(self, path):
        with open(path, "wb") as f:
            pickle.dump(self, f)

    @staticmethod
    def read_pkl_file(path):
        with open(path, "rb") as f:
            return pickle.load(f)

    def export_report_as_docx_file(self, path):
        doc = Document()
        doc.add_heading("Rapport d'intervention", 0)

        doc.add_heading("1. Introduction", level=1)
        doc.add_paragraph(f"Sujet : {self.report_subject}")
        doc.add_paragraph(f"Date : {self.intervention_date}")
        doc.add_paragraph(f"Zone : {self.intervention_zone}")
        doc.add_paragraph(f"Site : {self.site}")

        doc.add_heading("2. État des lieux", level=1)
        doc.add_paragraph(self.content["etat_des_lieux"])

        doc.add_heading("3. Diagnostic et évaluation des risques", level=1)
        doc.add_paragraph(self.content["diagnostic"])

        doc.add_heading("4. Préconisations", level=1)
        doc.add_paragraph(self.content["preconisation"])

        doc.save(path)


    def __str__(self):
        return f"{self.content['etat_des_lieux']}"