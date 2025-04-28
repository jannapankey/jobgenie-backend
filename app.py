# app.py

from flask import Flask, request, send_from_directory, jsonify
import os
from agent import run_resume_agent
from render import render_resume_html
from save import save_resume_as_docx

app = Flask(__name__)

# Save generated resumes to a downloads folder
DOWNLOAD_FOLDER = os.path.join(os.getcwd(), "downloads")
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

@app.route("/generate_resume", methods=["POST"])
def generate_resume():
    try:
        # Force parse JSON body
        data = request.get_json(force=True)

        if not data:
            return jsonify({"error": "No JSON body received."}), 400

        # Validate required fields
        required_fields = ["full_name", "email", "phone", "education", "skills", "job_description", "work_experiences"]
        missing_fields = [field for field in required_fields if field not in data]

        if missing_fields:
            return jsonify({
                "error": f"Missing required fields: {', '.join(missing_fields)}",
                "suggestion": "Make sure your Bubble API Connector is sending all necessary fields."
            }), 400

        # Validate work_experiences
        if not isinstance(data["work_experiences"], list):
            return jsonify({
                "error": "work_experiences must be a list.",
                "suggestion": "Even if the user has no work history, send an empty array [] for work_experiences."
            }), 400

        for exp in data["work_experiences"]:
            if not isinstance(exp, dict):
                return jsonify({"error": "Each work_experience must be an object."}), 400
            if "dates" not in exp or not isinstance(exp["dates"], list) or len(exp["dates"]) != 2:
                return jsonify({
                    "error": "Each work_experience must have a 'dates' array with exactly two elements: [start, end].",
                    "suggestion": "Example: [\"Jan 2020\", \"Dec 2022\"]"
                }), 400

        # Safely extract candidate info
        candidate_info = {
            "full_name": data.get("full_name", "Unknown Name"),
            "email": data.get("email", "Unknown Email"),
            "phone": data.get("phone", "Unknown Phone"),
            "education": data.get("education", "Unknown Education"),
            "skills": data.get("skills", ""),
            "work_experiences": data.get("work_experiences", [])
        }
        job_description = data.get("job_description", "")

        print("Received candidate info:", candidate_info)
        print("Received job description:", job_description)

        # Run agent pipeline
        final_resume_json = run_resume_agent(candidate_info, job_description)

        # Render for Bubble preview
        rendered_resume = render_resume_html(final_resume_json)

        # Save DOCX
        filename = f"{candidate_info['full_name'].replace(' ', '_')}_resume.docx"
        file_path = save_resume_as_docx(final_resume_json, filename)
        download_link = f"/download/{os.path.basename(file_path)}"

        return jsonify({
            "download_link": download_link,
            "resume_text": rendered_resume
        })

    except Exception as e:
        print("Error in generate_resume:", e)
        return jsonify({
            "error": str(e),
            "suggestion": "Check if all required fields are properly sent and formatted."
        }), 500

# Route to serve download files
@app.route("/download/<path:filename>", methods=["GET"])
def download_file(filename):
    return send_from_directory(DOWNLOAD_FOLDER, filename, as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)
