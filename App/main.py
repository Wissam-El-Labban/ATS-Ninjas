import streamlit as st
from langchain_community.document_loaders import WebBaseLoader
from gemini_client import OpenAIClient
from portfolio import Portfolio
from utils import clean_text
import os
os.chdir("D:\ATS-Ninjas\App")

def create_streamlit_app(llm, portfolio, clean_text):
    st.title("📧 Cold Mail & Cover Letter Generator")
    url_input = st.text_input("Enter a Job Posting URL:", value="")

    # Upload Resume File
    resume_file = st.file_uploader("Upload Your Resume", type=["pdf", "docx", "txt"])

    # Dropdown to choose content type
    content_type = st.selectbox("Select Content Type", ["Cold Email", "Cover Letter"])

    submit_button = st.button("Generate Content")

    if submit_button:
        try:
            loader = WebBaseLoader([url_input])
            raw_text = loader.load().pop().page_content
            data = clean_text(raw_text[:6000])  # Limit input to avoid context overflow
            portfolio.load_portfolio()

            # Load resume content
            if resume_file is not None:
                if resume_file.type == "application/pdf":
                    resume_content = extract_pdf_text(resume_file)
                elif resume_file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
                    resume_content = extract_docx_text(resume_file)
                elif resume_file.type == "text/plain":
                    resume_content = str(resume_file.read(), "utf-8")
                else:
                    st.error("Unsupported resume format")
                    return
            else:
                resume_content = ""

            # Call the LLM's job extraction function
            jobs = llm.extract_jobs(data)

            # 🧪 Optional: Show raw job JSON in UI for debugging
            with st.expander("🔍 View Extracted Jobs (Raw JSON)"):
                st.json(jobs)

            # ⚠️ Handle empty results gracefully
            if not jobs or (isinstance(jobs, list) and len(jobs) == 0):
                st.warning("No job postings were extracted. Please try a different URL or make sure the job text is visible.")
                return

            # 🔧 Flatten nested job lists if needed
            job = jobs[0]
            print(job)
            print(type(job))
            
            skills = job.get('skills', [])
            print("skills check \n")
            print(skills)
            #print(skills[0])
            print('\n')
            print(type(skills))
            print(skills[0])
            #links = portfolio.query_links(skills)
            links = skills[0]

            job_description = job.get("description")
            #job_description = job.get("description", "No description available.")  # If description is missing, use a default string
            #print(f"Processing job: {job.get('role')}")  # Debugging statement to track the job being processed

            print("still alive")

                # Generate based on selected content type
            if content_type == "Cold Email":
                content = llm.write_mail(job_description, links)
                st.code(content, language='markdown')

            elif content_type == "Cover Letter":
                content = llm.write_cover_letter(resume_content, job_description, links)
                st.code(content, language='markdown')

                # Save as Word document
                filename = llm.save_cover_letter(content)
                with open(filename, "rb") as file:
                    st.download_button(
                        label="Download Cover Letter",
                        data=file,
                        file_name=filename,
                        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                    )

        except Exception as e:
            st.error(f"An Error Occurred: {e}")

# Helper function to extract text from a PDF file
def extract_pdf_text(pdf_file):
    from PyPDF2 import PdfReader
    reader = PdfReader(pdf_file)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text

# Helper function to extract text from a DOCX file
def extract_docx_text(docx_file):
    from docx import Document
    doc = Document(docx_file)
    text = ""
    for para in doc.paragraphs:
        text += para.text + "\n"
    return text

if __name__ == "__main__":
    chain = OpenAIClient()
    portfolio = Portfolio()
    st.set_page_config(layout="wide", page_title="Cold Email & Cover Letter Generator", page_icon="📧")
    create_streamlit_app(chain, portfolio, clean_text)
