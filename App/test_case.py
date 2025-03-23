import os
import json
import requests
import google.generativeai as genai
from langchain.document_loaders import WebBaseLoader
import os
from dotenv import load_dotenv
load_dotenv()

os.chdir("D:\ATS-Ninjas\App")

def clean_text(text):
    return " ".join(text.split())

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

        ⚠️ Return only the JSON. No additional text, no explanations. do not include json in your response.

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
            response_text = response.text.strip()
            response_text = str(response_text)
            print(type(response_text))
            response_text = response_text.replace("json", "")
            response_text = response_text[3:-3].strip()
            print("test below\n")
            print(response_text)
            return json.loads(response_text)
        except json.JSONDecodeError:
            raise ValueError("❌ Gemini returned invalid JSON:\n\n" + response_text)


def scrape_website(url):
    loader = WebBaseLoader([url])
    raw_text = loader.load().pop().page_content
    return clean_text(raw_text[:6000])  # Limit input to avoid context overflow


def main():
    #url = input("Enter the job listing URL: ")
    url = "https://search-careers.gm.com/en/jobs/jr-202505151/staff-data-engineer/"
    try:
        scraped_text = scrape_website(url)
        #portfolio.load_portfolio()
        gemini_client = GeminiClient()
        jobs = gemini_client.extract_jobs(scraped_text)
        print(json.dumps(jobs, indent=2))
    except Exception as e:
        print("Error:", e)


if __name__ == "__main__":
    main()