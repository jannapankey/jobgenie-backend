# In render.py

def render_resume_html(resume_json, full_name="Unknown", email="Unknown", phone="Unknown"):
    summary = resume_json.get("summary", "")
    education = resume_json.get("education", "")
    skills_list = resume_json.get("skills", [])
    skills = ", ".join(skills_list)
    experiences = resume_json.get("experience", [])

    html = f"""
    <h1>{full_name}</h1>
    <p>Email: {email} | Phone: {phone}</p>

    <h1>Professional Summary</h1>
    <p>{summary}</p>

    <h1>Education</h1>
    <p>{education}</p>

    <h1>Skills</h1>
    <p>{skills}</p>

    <h1>Experience</h1>
    """

    for exp in experiences:
        title = exp.get("title", "")
        company = exp.get("company", "")
        dates = exp.get("dates", "")
        bullets = exp.get("bullets", [])

        html += f"""
        <h2>{title} at {company} ({dates})</h2>
        <ul>
        """
        for bullet in bullets:
            html += f"<li>{bullet}</li>"
        html += "</ul>"

    return html
