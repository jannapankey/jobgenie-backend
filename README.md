Team Members: Xavier Alleyne, Nana Amoah, Janna Pankey, Tyler Trocchi, Jasmine Weekes

# JobGenie Backend

## Business Problem

Job seekers often struggle with creating tailored, ATS-optimized resumes that align with specific job descriptions. Manually rewriting and formatting resumes for each application is time-consuming, and generic resumes often fail to pass initial screening stages.

**Business Goal:**  
Automate the generation of high-quality, tailored resumes using generative AI and resume templates to streamline the job application process and improve applicant outcomes.

---

## Solution Architecture Overview

The system is composed of the following components:

- **Frontend (Bubble.io)**  
  A no-code interface that allows users to input personal details, upload job descriptions, preview generated resumes, and download them as Word documents.

- **Backend (Flask + Python)**  
  A hosted API that receives user input from Bubble, calls OpenAI’s `gpt-4-turbo` model to generate resume content in structured JSON format, renders the data into a `.docx` file using `python-docx`, and converts the file to HTML for preview inside Bubble.

- **LLM Integration (OpenAI)**  
  OpenAI's GPT model is used to generate a 5-sentence professional summary, a list of relevant skills, an education summary, and work experience formatted as job entries with at least 3 bullet points.

- **Document Generation**  
  Uses `python-docx` to create Word documents and `beautifulsoup4` to parse HTML for accurate formatting during conversion.

---

## Setup and Deployment Instructions

**Local Development:**

1. Clone the repository:
   ```bash
   git clone https://github.com/your-team/jobgenie-backend.git
   cd jobgenie-backend
   ```

2. Create a `.env` file:
   ```
   OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxxxxxx
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Run the application:
   ```bash
   flask run
   ```

**Deployment:**

- The backend is deployed on [Render](https://render.com) using `gunicorn` with:
   ```bash
   gunicorn app:app
   ```

**Frontend Setup:**

- Built using Bubble.io
- API Connector plugin is configured to call the `/generate_resume` endpoint
- Resume text is passed to `document_viewer` via URL parameters for preview
- Full download link is dynamically generated and opened for resume download

---

## Use of LLMs and Changes to Agent Architecture

**LLM Used:**  
OpenAI’s `gpt-4-turbo`

**Purpose:**  
Generate ATS-optimized resumes including a summary, skills, education, and bullet-pointed work experience.

**Evolution of the Agent System:**

- **Original System:**  
  - Started with a **single LLM call** responsible for analyzing, completing, drafting, and improving the resume.
  - **Problem:** The LLM often got "lost" — mixing responsibilities, hallucinating sections, and returning incomplete outputs.

- **Then Moved to Single Agent Approach:**  
  - One combined agent designed to follow all steps carefully in sequence.
  - **Problem:** Still unstable — would lose track when handling multiple tasks at once.

- **Introduced 4 Agents:**  
  - Analyze Candidate Info
  - Fill Missing Pieces
  - Draft Resume
  - Review and Improve Resume
  - Each agent had a narrow, focused task.
  - **Problem:** Too many API calls led to longer response times and higher costs.

- **Final System:**  
  - Consolidated into **3 agents**:
    1. Analyze + Fill Missing Info
    2. Draft Resume
    3. Review and Improve Resume
  - **Benefits:** Faster processing, lower cost, better control over LLM outputs.

**Reasons for Changes:**
- **Stability:** Single or all-in-one LLM approaches tended to get "lost" across multi-step logic.
- **Control:** Breaking steps down improved predictability and JSON output consistency.
- **Efficiency:** Reducing from 4 to 3 agents significantly cut down response time and token usage.

**Challenges:**
- Ensuring consistent and valid JSON output formatting.
- Managing incomplete or messy user input (e.g., missing work experience, missing education fields).
- Preventing the model from hallucinating invented experiences or unrealistic skills.
- Balancing creativity (to fill missing info) while maintaining resume realism and professionalism.
- Synchronizing the resume preview inside Bubble with the final downloadable Word file formatting.

---

## No-Code Integration (Bubble.io)

Bubble.io was used to:

- Collect user input for personal info and job description
- Call the Flask backend using the API Connector plugin
- Display the resume preview in a scrollable HTML element
- Allow users to download the final `.docx` resume via a direct file link

**Why Bubble:**  
It enabled rapid prototyping of a professional frontend without writing traditional frontend code, and integrated seamlessly with a custom Python backend.

**Enhancements Implemented:**
- Preview rendered resumes directly inside Bubble using HTML.
- Download resumes without opening a new webpage using dynamic links.
- Improved user experience by ensuring name, email, and phone data populate correctly in both preview and final Word file.

---
