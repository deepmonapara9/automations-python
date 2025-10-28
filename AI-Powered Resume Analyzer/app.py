import streamlit as st
import pdfplumber, docx, subprocess, pandas as pd
from datetime import datetime
import os, re
import tempfile, io

# configs
MODEL = "mistral"
CSV_FILE = "resume_analysis.csv"


# utils
# This function extracts text from PDF or DOCX files
def extract_text(file):
    ext = os.path.splitext(file.name)[1].lower()
    text = ""

    try:
        # Reset file pointer to beginning
        file.seek(0)
        file_content = file.read()

        with tempfile.NamedTemporaryFile(delete=False, suffix=ext) as tmp:
            tmp.write(file_content)
            tmp.flush()
            tmp_path = tmp.name

        if ext == ".pdf":
            with pdfplumber.open(tmp_path) as pdf:
                for page in pdf.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n"
        elif ext == ".docx":
            try:
                doc = docx.Document(tmp_path)
                for paragraph in doc.paragraphs:
                    text += paragraph.text + "\n"
            except Exception as docx_error:
                st.error(f"Error reading DOCX file: {docx_error}")
                return ""
        else:
            st.error("Unsupported file format. Please upload PDF or DOCX.")
            return ""

    except Exception as e:
        st.error(f"Error processing file: {e}")
        return ""
    finally:
        try:
            if "tmp_path" in locals() and os.path.exists(tmp_path):
                os.remove(tmp_path)
        except:
            pass

    return text.strip()


# This function interacts with the Ollama model to analyze the resume text
def analyze_with_ollama(text):
    prompt = f"""
    You are an AI resume reviewer. Analyze the resume and provide a concise summary in this exact format:

    Name: [Full name of the candidate]
    Email: [Email address]
    Skills: [List top 5-8 key technical skills, separated by commas]
    Experience: [Total years of experience and current/recent role summary in 1-2 sentences]
    Summary: [Brief 2-3 sentence professional summary]
    Score: [Overall rating out of 10 based on skills, experience, and presentation]

    Resume Text:
    {text}
    
    Please keep each field concise and focused. For Experience, only mention years of experience and current role, not the entire job history.
    """
    try:
        result = subprocess.run(
            ["ollama", "run", MODEL],
            input=prompt,
            text=True,
            capture_output=True,
            timeout=60,  # Add timeout to prevent hanging
        )
        if result.returncode != 0:
            st.error(f"Ollama error: {result.stderr}")
            return ""
        return result.stdout.strip()
    except subprocess.TimeoutExpired:
        st.error("Analysis timed out. Please try again.")
        return ""
    except Exception as e:
        st.error(f"Error running Ollama: {e}")
        return ""


# This function parses the output from the Ollama model
def parse_output(output):
    """Extracts structured fields from the Ollama output with flexible matching."""
    data = {"Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
    lines = output.split("\n")

    patterns = {
        "Name": r"(?:name|candidate name)[\s:-]+(.+?)(?:\n|$)",
        "Email": r"(?:email)[\s:-]+([\w\.-]+@[\w\.-]+)",
        "Skills": r"(?:skills?|technologies|proficiencies)[\s:-]+(.+?)(?:\n(?:[A-Z][a-z]+:|$)|$)",
        "Experience": r"(?:experience|years of experience)[\s:-]+(.+?)(?:\n(?:[A-Z][a-z]+:|$)|$)",
        "Summary": r"(?:summary|profile)[\s:-]+(.+?)(?:\n(?:[A-Z][a-z]+:|$)|$)",
        "Score": r"(?:score|rating)[\s:-]+(\d+(?:\.\d+)?)",
    }

    for key, pattern in patterns.items():
        match = re.search(pattern, output, re.IGNORECASE | re.DOTALL)
        if match:
            extracted = match.group(1).strip()
            if key == "Experience":
                sentences = extracted.split(".")
                if sentences:
                    extracted = sentences[0].strip()
                    if len(extracted) > 150:
                        extracted = extracted[:150] + "..."
            elif key in ["Skills", "Summary"]:
                if len(extracted) > 200:
                    extracted = extracted[:200] + "..."
            data[key] = extracted
        else:
            data[key] = ""

    return data


# This function saves the parsed data to a CSV file
def save_to_csv(data):
    df = pd.DataFrame([data])
    file_exists = os.path.isfile(CSV_FILE)
    df.to_csv(CSV_FILE, mode="a", index=False, header=not file_exists)
    st.success("Data saved to resume_analysis.csv!")


# streamlit app
st.set_page_config(
    page_title="Ollama Resume Analyzer", page_icon="🧠", layout="centered"
)
st.title("AI-Powered Resume Analyzer (Local Ollama)")
st.caption("Upload resumes, extract details, and analyze them locally using Ollama.")

uploaded_file = st.file_uploader("Upload Resume (PDF/DOCX)", type=["pdf", "docx"])

if uploaded_file:
    with st.spinner("Extracting text..."):
        text = extract_text(uploaded_file)

    if text:
        st.subheader("Extracted Resume Text")
        st.text_area("Preview", text, height=200)

        if st.button("Analyze with Ollama"):
            with st.spinner("Analyzing resume using Ollama..."):
                analysis = analyze_with_ollama(text)
                st.subheader("Analysis Result")
                st.text(analysis)

                parsed_data = parse_output(analysis)
                st.json(parsed_data)
                save_to_csv(parsed_data)

# view logs
st.markdown("---")
if st.checkbox("Show Resume Analysis Log"):
    if os.path.exists(CSV_FILE):
        df = pd.read_csv(CSV_FILE)
        st.dataframe(df)
        if "Score" in df.columns:
            try:
                df["Score"] = pd.to_numeric(df["Score"], errors="coerce")
                st.bar_chart(df["Score"].dropna())
            except:
                pass
    else:
        st.info("No analysis logs found yet.")
