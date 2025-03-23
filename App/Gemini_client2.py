import os
import json
import google.generativeai as genai
from dotenv import load_dotenv

os.chdir("D:\ATS-Ninjas\App")
load_dotenv()

class GeminiClient:
    def __init__(self):
        genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
        self.model = genai.GenerativeModel("models/gemini-2.0-pro-exp-02-05")

    def extract_jobs(self, cleaned_text):
        prompt = f"""
        You are an expert at parsing job descriptions from websites.

        ### SCRAPED TEXT:
        {cleaned_text}

        ### TASK:
        Extract all job postings in JSON format. Each job must include:
        - "role": the job title
        - "experience": years or type of experience required
        - "skills": a list of relevant skills
        - "description": the job summary

        ⚠️ Return only the JSON. No additional text, no explanations.

        ### EXAMPLE FORMAT:
        [
          {{
            "role": "Data Analyst",
            "experience": "2+ years in data analysis",
            "skills": ["SQL", "Python", "Tableau"],
            "description": "Analyze business metrics and deliver insights."
          }}
        ]
        """
        response = self.model.generate_content(prompt)
        try:
            #return json.loads(response.text.strip())
            response_text = response.text.strip()
            response_text = str(response_text)
            print(type(response_text))
            response_text = response_text.replace("json", "")
            response_text = response_text[3:-3].strip()
            print("test below\n")
            print(response_text)
            return json.loads(response_text)
        except json.JSONDecodeError:
            raise ValueError("❌ Gemini returned invalid JSON:\n\n" + response.text)

    def write_mail(self, job_description, links):
        prompt = f"""
        ### JOB DESCRIPTION:
        {job_description}

        ### TASK:
        Write a cold email to HR from Pradhum Niroula, MS Business Analytics student at Oakland University.
        Highlight why you're a great fit based on the job description and include relevant portfolio links:
        {links}

        Keep it short and professional. Do not include a greeting like "Hi, I'm Gemini."

        ### EMAIL (NO PREAMBLE):
        """
        response = self.model.generate_content(prompt)
        return response.text.strip()

    def write_cover_letter(self, resume, job_description, links):
        prompt = f"""
        ### TASK:
        Write a professional cover letter for Pradhum Niroula.

        Use the following:
        - Resume: {resume}
        - Job Description: {job_description}
        - Portfolio links: {links}

        Focus on qualifications, fit, and enthusiasm. Make it tailored, clear, and confident.

        ### COVER LETTER (NO PREAMBLE):
        """
        response = self.model.generate_content(prompt)
        return response.text.strip()