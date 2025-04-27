# agent.py

import openai
import os
from dotenv import load_dotenv
import json

# Load environment variables
load_dotenv()
client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))  # ✅ Correct client initialization

# Helper function: call OpenAI
def call_openai(messages, temperature=0.3):
    response = client.chat.completions.create(  # ✅ Use client.chat.completions.create
        model="gpt-4-turbo",
        messages=messages,
        temperature=temperature,
        max_tokens=3000
    )
    return response.choices[0].message.content  # ✅ New object attribute access

# Agent Step 1: Analyze Candidate Info
def agent_analyze(candidate_info, job_description):
    messages = [
        {"role": "system", "content": "You are an expert career coach. Your task is to analyze the candidate's information and detect if any critical fields (work experience, skills, education) are missing or weak. Respond with a clear JSON list of issues you find."},
        {"role": "user", "content": f"Candidate Info: {candidate_info}\nTarget Job Description: {job_description}"}
    ]
    analysis = call_openai(messages)
    return analysis

# Agent Step 2: Fill Missing Pieces
def agent_fill_missing(candidate_info, job_description, analysis):
    messages = [
        {"role": "system", "content": "You are a resume builder agent. Based on the candidate info and detected issues, intelligently fill missing fields. Invent realistic entry-level work experience if missing. Suggest relevant skills based on the job description."},
        {"role": "user", "content": f"Candidate Info: {candidate_info}\nDetected Issues: {analysis}\nTarget Job Description: {job_description}"}
    ]
    filled_info = call_openai(messages)
    return filled_info

# Agent Step 3: Draft Full Resume
def agent_draft_resume(filled_info, job_description):
    messages = [
        {"role": "system", "content": "You are a professional resume writer. Based on the completed candidate information, draft a polished, ATS-optimized resume in this exact JSON format:\n\n{\n  \"summary\": \"5 sentence professional summary tailored to job description.\",\n  \"skills\": [\"Skill 1\", \"Skill 2\", \"Skill 3\"],\n  \"education\": \"Degree, School, Year\",\n  \"experience\": [\n    {\n      \"title\": \"Job Title\",\n      \"company\": \"Company Name\",\n      \"dates\": \"Start – End\",\n      \"bullets\": [\n        \"Action-oriented achievement bullet 1.\",\n        \"Bullet 2.\",\n        \"Bullet 3.\"\n      ]\n    }\n  ]\n}\n\nRespond only with the JSON."},
        {"role": "user", "content": f"Final Candidate Info: {filled_info}\nTarget Job Description: {job_description}"}
    ]
    resume_json_text = call_openai(messages)
    try:
        resume_json = json.loads(resume_json_text)
    except json.JSONDecodeError:
        raise ValueError("Agent Draft failed to produce valid JSON. Raw output:\n" + resume_json_text)
    return resume_json

# Agent Step 4: Review and Improve Resume
def agent_review_and_improve(resume_json, job_description):
    messages = [
        {"role": "system", "content": "You are a resume reviewer agent. Review the resume JSON carefully. Make improvements to better tailor it to the target job description. Ensure:\n- 5 full sentences in the professional summary\n- Each job has at least 3 strong bullets\n- Skills match job description\nReturn only the final corrected JSON."},
        {"role": "user", "content": f"Resume JSON: {json.dumps(resume_json)}\nTarget Job Description: {job_description}"}
    ]
    improved_json_text = call_openai(messages)
    try:
        improved_resume_json = json.loads(improved_json_text)
    except json.JSONDecodeError:
        raise ValueError("Agent Review failed to produce valid JSON. Raw output:\n" + improved_json_text)
    return improved_resume_json

# Main Chain: Run Full Multi-Agent Process
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
