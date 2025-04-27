# app.py

from flask import Flask, request, jsonify, send_from_directory
import os
import uuid
from agent import run_resume_agent
from docxtpl import DocxTemplate
import mammoth
from dotenv import load_dotenv

load_dotenv()

import openai
openai.api_key = os.getenv("OPENAI_API_KEY")


app = Flask(__name__)
DOWNLOAD_FOLDER = "downloads"
TEMPLATE_PATH = "templates/resume_template.docx"
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

def convert_docx_to_html(filepath):
    with open(filepath, "rb") as docx_file:
        result = mammoth.convert_to_html(docx_file)
        return result.value

@app.route("/generate", methods=["POST"])
def generate_resume():
    try:
        data = request.get_json(force=True)

        full_name = data.get("full_name", "")
        email = data.get("email", "")
        phone = data.get("phone", "")
        education = data.get("education", "")
        skills = data.get("skills", "")
        job_description = data.get("job_description", "")
        work_experiences = data.get("work_experiences", [])

        candidate_info = {
            "full_name": full_name,
            "email": email,
            "phone": phone,
            "education": education,
            "skills": skills,
            "work_experiences": work_experiences
        }

        # Run Agent
        resume_json = run_resume_agent(candidate_info, job_description)

        # Select first job for template fill
        first_job = resume_json.get("experience", [{}])[0]

        # Fill docx template
        template = DocxTemplate(TEMPLATE_PATH)
        template.render({
            "FULL_NAME": full_name or "Candidate Name",
            "EMAIL": email or "",
            "PHONE": phone or "",
            "PROFESSIONAL_SUMMARY": resume_json.get("summary", "Summary not available."),
            "EDUCATION": resume_json.get("education", "Education not available."),
            "SKILLS": "\n".join(resume_json.get("skills", ["Skills not listed."])),
            "EXPERIENCE": "\n".join(first_job.get("bullets", ["Experience details not available."])),
            "COMPANY": first_job.get("company", ""),
            "JOB_TITLE": first_job.get("title", ""),
            "START_DATE": first_job.get("dates", "").split("–")[0].strip() if "–" in first_job.get("dates", "") else "",
            "END_DATE": first_job.get("dates", "").split("–")[1].strip() if "–" in first_job.get("dates", "") else ""
        })

        file_id = str(uuid.uuid4())
        file_path = os.path.join(DOWNLOAD_FOLDER, f"{file_id}.docx")
        template.save(file_path)

        # HTML preview
        resume_html = convert_docx_to_html(file_path)

        return jsonify({
            "resume_text": resume_html,
            "download_link": f"https://jobgenie-backend.onrender.com/download/{file_id}.docx"
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route("/download/<filename>")
def download(filename):
    return send_from_directory(DOWNLOAD_FOLDER, filename, as_attachment=True)
