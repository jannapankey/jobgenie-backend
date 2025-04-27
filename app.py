# app.py

from flask import Flask, request, send_from_directory, jsonify
import os
from agent import run_resume_agent
from docxtpl import DocxTemplate
from mammoth import convert_to_html
import tempfile

app = Flask(__name__)

# Save generated resumes to a downloads folder
DOWNLOAD_FOLDER = os.path.join(os.getcwd(), "downloads")
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

@app.route("/generate", methods=["POST"])
def generate_resume():
    try:
        # 1. Get the incoming JSON body
        data = request.get_json()

        full_name = data.get("full_name")
        email = data.get("email")
        phone = data.get("phone")
        education = data.get("education")
        skills = data.get("skills")
        job_description = data.get("job_description")
        work_experiences = data.get("work_experiences", [])

        # 2. Organize candidate info
        candidate_info = {
            "full_name": full_name,
            "email": email,
            "phone": phone,
            "education": education,
            "skills": skills,
            "work_experiences": work_experiences
        }

        # 3. Run the agent process
        final_resume = run_resume_agent(candidate_info, job_description)

        # 4. Load Word template
        doc = DocxTemplate("templates/resume_template.docx")

        context = {
            "full_name": full_name,
            "email": email,
            "phone": phone,
            "summary": final_resume["summary"],
            "skills": ', '.join(final_resume["skills"]),
            "education": final_resume["education"],
            "experience": final_resume["experience"]
        }

        # 5. Render and save .docx
        output_filename = f"{full_name.replace(' ', '_')}_resume.docx"
        output_path = os.path.join(DOWNLOAD_FOLDER, output_filename)
        doc.render(context)
        doc.save(output_path)

        # 6. Convert to HTML for Preview
        with open(output_path, "rb") as docx_file:
            result = convert_to_html(docx_file)
            resume_html = result.value

        # 7. Return proper JSON (IMPORTANT)
        return jsonify({
            "download_link": f"/download/{output_filename}",
            "resume_text": resume_html
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route("/download/<path:filename>")
def download_file(filename):
    return send_from_directory(DOWNLOAD_FOLDER, filename, as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)
