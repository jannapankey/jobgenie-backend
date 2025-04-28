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
        # 1. Receive candidate info
        data = request.get_json()
        print("Received candidate info:", data)

        # SAFELY extract fields with defaults if missing
        full_name = data.get("full_name") or "Unknown Candidate"
        email = data.get("email") or "unknown@example.com"
        phone = data.get("phone") or "Unknown Phone"
        education = data.get("education") or "Education not provided"
        skills = data.get("skills") or "Skills not provided"
        job_description = data.get("job_description") or "Job description not provided"

        # Handle work_experiences safely
        work_experiences = data.get("work_experiences", [])
        cleaned_work_experiences = []
        for exp in work_experiences:
            if exp:
                cleaned_work_experiences.append({
                    "job_title": exp.get("job_title", "No Title Provided"),
                    "company": exp.get("company", "No Company Provided"),
                    "dates": exp.get("dates", ["No Start", "No End"]),
                    "description": exp.get("description", "No Description Provided")
                })

        candidate_info = {
            "full_name": full_name,
            "email": email,
            "phone": phone,
            "education": education,
            "skills": skills,
            "work_experiences": cleaned_work_experiences
        }

        print("Cleaned candidate info:", candidate_info)
        print("Received job description:", job_description)

        # 2. Run the multi-agent process
        print("Step 1: Analyzing candidate info...")
        print("Step 2: Filling missing information...")
        print("Step 3: Drafting resume...")
        print("Step 4: Reviewing and improving resume...")
        final_resume_json = run_resume_agent(candidate_info, job_description)
        print("Generated resume JSON:", final_resume_json)

        # 3. Render HTML for Bubble preview
        rendered_resume = render_resume_html(final_resume_json, full_name, email, phone)

        # 4. Save Word doc
        safe_name = full_name.replace(" ", "_") or "Unknown_Candidate"
        filename = f"{safe_name}_resume.docx"
        file_path = save_resume_as_docx(final_resume_json, filename)

        # 5. Create download link
        download_link = f"https://jobgenie-backend-1.onrender.com/download/{os.path.basename(file_path)}"

        # 6. Return the result
        return jsonify({
            "download_link": download_link,
            "resume_text": rendered_resume
        })

    except Exception as e:
        print("Error in generate_resume:", e)
        return jsonify({"error": str(e)}), 500

# Route to serve downloaded files
@app.route("/download/<filename>")
def download_file(filename):
    try:
        return send_from_directory(DOWNLOAD_FOLDER, filename, as_attachment=True)
    except FileNotFoundError:
        return jsonify({"error": "File not found"}), 404

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))