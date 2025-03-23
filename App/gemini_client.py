import os
import json
import openai
from dotenv import load_dotenv

os.chdir("D:\ATS-Ninjas\App")

load_dotenv()

class OpenAIClient:
    def __init__(self):
        openai.api_key = os.getenv("OPENAI_API_KEY")
        self.model = "gpt-4"

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
        response = openai.ChatCompletion.create(
            model=self.model,
            messages=[
                {"role": "system", "content": "You are an expert at parsing job descriptions."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=1500,
            temperature=0.7
        )

        try:
            response_text = response['choices'][0]['message']['content'].strip()
            response_text = response_text.replace("json", "").strip()
            return json.loads(response_text)
        except json.JSONDecodeError:
            raise ValueError("❌ GPT-4 returned invalid JSON:\n\n" + response['choices'][0]['message']['content'])

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
        response = openai.ChatCompletion.create(
            model=self.model,
            messages=[
                {"role": "system", "content": "You are an expert at writing professional emails."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=500,
            temperature=0.7
        )

        return response['choices'][0]['message']['content'].strip()

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
        response = openai.ChatCompletion.create(
            model=self.model,
            messages=[
                {"role": "system", "content": "You are an expert at writing professional cover letters."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=1000,
            temperature=0.7
        )

        return response['choices'][0]['message']['content'].strip()