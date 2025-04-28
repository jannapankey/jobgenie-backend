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

# Step 1: Analyze Candidate Info
def agent_analyze(candidate_info, job_description):
    messages = [
        {"role": "system", "content": "You are an expert career coach. Analyze the candidate's info and detect missing or weak fields (work experience, skills, education). Respond ONLY with a clear JSON list of issues you find."},
        {"role": "user", "content": f"Candidate Info: {candidate_info}\nJob Description: {job_description}"}
    ]
    analysis = call_openai(messages)
    return analysis

# Step 2: Fill Missing Pieces
def agent_fill_missing(candidate_info, job_description, analysis):
    messages = [
        {"role": "system", "content": "You are a resume builder agent. Based on candidate info and detected issues, intelligently fill missing fields. Invent realistic entry-level experience if needed. Suggest relevant skills based on the job."},
        {"role": "user", "content": f"Candidate Info: {candidate_info}\nDetected Issues: {analysis}\nJob Description: {job_description}"}
    ]
    filled_info = call_openai(messages)
    return filled_info

# Step 3: Draft Resume
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

# Step 4: Review and Improve Resume
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
    print("Step 1: Analyzing candidate info...")
    analysis = agent_analyze(candidate_info, job_description)

    print("Step 2: Filling missing information...")
    filled_info = agent_fill_missing(candidate_info, job_description, analysis)

    print("Step 3: Drafting resume...")
    draft_resume = agent_draft_resume(filled_info, job_description)

    print("Step 4: Reviewing and improving resume...")
    final_resume = agent_review_and_improve(draft_resume, job_description)

    return final_resume
