import openai
import os
import json
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize OpenAI client
client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Helper function: call OpenAI Chat API
def call_openai(messages, temperature=0.3):
    response = client.chat.completions.create(
        model="gpt-4-turbo",
        messages=messages,
        temperature=temperature,
        max_tokens=3000
    )
    return response.choices[0].message.content

# Step 1: Analyze and Fill Missing Pieces (Combined)
def agent_analyze_and_fill(candidate_info, job_description):
    messages = [
        {"role": "system", "content": "You are an expert resume assistant. Analyze the candidate's information and detect missing or weak fields (work experience, skills, education). Then immediately fill missing fields by inventing realistic, entry-level experience and suggesting relevant skills based on the job description. Return ONLY the completed candidate information, ready for resume drafting."},
        {"role": "user", "content": f"Candidate Info: {candidate_info}\nJob Description: {job_description}"}
    ]
    filled_info = call_openai(messages)
    return filled_info

# Step 2: Draft Resume
def agent_draft_resume(filled_info, job_description):
    messages = [
        {"role": "system", "content": "You are a professional resume writer. Based on completed candidate info, draft an ATS-optimized resume in EXACTLY this JSON format:\n\n{\n  \"summary\": \"5-sentence professional summary.\",\n  \"skills\": [\"Skill1\", \"Skill2\", \"Skill3\"],\n  \"education\": \"Degree, School, Year\",\n  \"experience\": [\n    {\n      \"title\": \"Job Title\",\n      \"company\": \"Company\",\n      \"dates\": \"Start-End\",\n      \"bullets\": [\"Achievement bullet 1.\", \"Bullet 2.\", \"Bullet 3.\"]\n    }\n  ]\n}\n\nRespond ONLY with valid JSON."},
        {"role": "user", "content": f"Candidate Info: {filled_info}\nJob Description: {job_description}"}
    ]
    resume_json_text = call_openai(messages)
    try:
        resume_json = json.loads(resume_json_text)
    except json.JSONDecodeError:
        raise ValueError("Failed to parse resume JSON. Raw output:\n" + resume_json_text)
    return resume_json

# Step 3: Review and Improve Resume
def agent_review_and_improve(resume_json, job_description):
    messages = [
        {"role": "system", "content": "You are a resume reviewer. Improve this resume JSON to better match the job. Ensure:\n- 5 full sentences in the summary\n- At least 3 strong bullets per job\n- Skills match job description\nReturn only the FINAL corrected JSON."},
        {"role": "user", "content": f"Resume JSON: {json.dumps(resume_json)}\nJob Description: {job_description}"}
    ]
    improved_json_text = call_openai(messages)
    try:
        improved_resume_json = json.loads(improved_json_text)
    except json.JSONDecodeError:
        raise ValueError("Failed to parse improved resume JSON. Raw output:\n" + improved_json_text)
    return improved_resume_json

# Main: Run the full agent chain
def run_resume_agent(candidate_info, job_description):
    print("Step 1: Analyzing and filling candidate info...")
    filled_info = agent_analyze_and_fill(candidate_info, job_description)

    print("Step 2: Drafting resume...")
    draft_resume = agent_draft_resume(filled_info, job_description)

    print("Step 3: Reviewing and improving resume...")
    final_resume = agent_review_and_improve(draft_resume, job_description)

    return final_resume
