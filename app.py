# app.py

from flask import Flask, request, send_from_directory, jsonify
import os
from agent import run_resume_agent
from render import render_resume_html  # Import from render.py
from save import save_resume_as_docx   # Import from save.py

app = Flask(__name__)

# Save generated resumes to a downloads folder
DOWNLOAD_FOLDER = os.path.join(os.getcwd(), "downloads")
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

@app.route("/generate_resume", methods=["POST"])
def generate_resume():
    try:
        # 1. Receive candidate info
        data = request.get_json()
        print("Received candidate info:", data)

        candidate_info = {
            "full_name": data.get("full_name"),
            "email": data.get("email"),
            "phone": data.get("phone"),
            "education": data.get("education"),
            "skills": data.get("skills"),
            "work_experiences": data.get("work_experiences", [])
        }
        job_description = data.get("job_description")

        print("Received job description:", job_description)

        # 2. Run the multi-agent process
        print("Step 1: Analyzing candidate info...")
        print("Step 2: Filling missing information...")
        print("Step 3: Drafting resume...")
        print("Step 4: Reviewing and improving resume...")
        final_resume_json = run_resume_agent(candidate_info, job_description)
        print("Generated resume JSON:", final_resume_json)

        # 3. Render HTML for Bubble preview
        rendered_resume = render_resume_html(final_resume_json)

        # 4. Save Word doc
        filename = f"{candidate_info['full_name'].replace(' ', '_')}_resume.docx"
        file_path = save_resume_as_docx(final_resume_json, filename)

        # 5. Create download link
        download_link = f"/download/{os.path.basename(file_path)}"

        # 6. Return the result
        return jsonify({
            "download_link": download_link,
            "resume_text": rendered_resume
        })

    except Exception as e:
        print("Error in generate_resume:", e)
        return jsonify({"error": str(e)}), 500

# Route to serve downloads
@app.route("/download/<path:filename>", methods=["GET"])
def download_file(filename):
    return send_from_directory(DOWNLOAD_FOLDER, filename, as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)
