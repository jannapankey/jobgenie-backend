# render.py

def render_resume_html(resume_json):
    html = ""

    # Professional Summary
    html += "<h1>Professional Summary</h1>\n"
    html += f"<p>{resume_json['summary']}</p>\n"

    # Education
    html += "<h1>Education</h1>\n"
    html += f"<p>{resume_json['education']}</p>\n"

    # Skills
    html += "<h1>Skills</h1>\n"
    html += f"<p>{', '.join(resume_json['skills'])}</p>\n"

    # Experience
    html += "<h1>Experience</h1>\n"
    for exp in resume_json['experience']:
        html += f"<h2>{exp['title']} at {exp['company']} ({exp['dates']})</h2>\n"
        html += "<ul>\n"
        for bullet in exp['bullets']:
            html += f"<li>{bullet}</li>"
        html += "</ul>\n"

    return html
