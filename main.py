import os
import shutil
import zipfile
import fitz  # PyMuPDF
import spacy
import re
from fastapi import FastAPI, UploadFile, File, Form
from fastapi.responses import FileResponse, HTMLResponse, Response
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from transformers import pipeline

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATES_DIR = os.path.join(BASE_DIR, "portfolio_templates")
OUTPUT_DIR = os.path.join(BASE_DIR, "generated_sites")
STATIC_DIR = os.path.join(BASE_DIR, "static")
HTML_TEMPLATE_DIR = os.path.join(BASE_DIR, "templates")

os.makedirs(TEMPLATES_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(STATIC_DIR, exist_ok=True)
os.makedirs(HTML_TEMPLATE_DIR, exist_ok=True)

app = FastAPI()
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

try:
    nlp = spacy.load("en_core_web_sm")
except:
    os.system("python -m spacy download en_core_web_sm")
    nlp = spacy.load("en_core_web_sm")

summarizer = pipeline("summarization", model="sshleifer/distilbart-cnn-12-6")

def parse_and_summarize(text):
    doc = nlp(text)
    
    # Filter out Names, Organizations, and Dates from skills
    excluded_labels = ["PERSON", "ORG", "DATE", "GPE", "TIME"]
    entities_to_exclude = [ent.text.lower() for ent in doc.ents if ent.label_ in excluded_labels]
    
    # Extract nouns and proper nouns that aren't personal names
    found_skills = []
    for token in doc:
        text_clean = token.text.strip()
        if (token.pos_ in ["PROPN", "NOUN"] and 
            len(text_clean) > 2 and 
            text_clean.lower() not in entities_to_exclude):
            found_skills.append(text_clean)
    
    # Remove duplicates while preserving order
    skills = list(dict.fromkeys(found_skills))[:12]
    
    # Better text cleaning for the summarizer
    clean_text = re.sub(r'\s+', ' ', text).strip()[:1200]
    summary = summarizer(clean_text, max_length=60, min_length=30, do_sample=False)
    
    return {"bio": summary[0]['summary_text'], "skills": skills}

@app.get("/", response_class=HTMLResponse)
async def root():
    html_path = os.path.join(HTML_TEMPLATE_DIR, "index.html")
    with open(html_path, "r") as f:
        content = f.read()
    return Response(content=content, media_type="text/html")

@app.post("/generate")
async def generate(file: UploadFile = File(...), theme: str = Form(...), primary_color: str = Form("#00d2ff")):
    pdf_bytes = await file.read()
    doc = fitz.open(stream=pdf_bytes, filetype="pdf")
    raw_text = " ".join([page.get_text() for page in doc])
    
    ml_results = parse_and_summarize(raw_text)
    job_id = f"job_{os.urandom(3).hex()}"
    user_dir = os.path.join(OUTPUT_DIR, job_id)
    os.makedirs(user_dir, exist_ok=True)
    
    template_path = os.path.join(TEMPLATES_DIR, theme, "index.html")
    with open(template_path, "r") as f:
        html = f.read()
    
    # Theme-specific container logic [cite: 1]
    theme_configs = {
        "neo": {"class": "pill", "container": '<div class="skills">'},
        "gloss": {"class": "skill-chip", "container": '<div class="skills-grid">'},
        "glass": {"class": "skill-chip", "container": '<div class="skills">'}
    }
    config = theme_configs.get(theme, theme_configs["glass"])
    
    skills_html = "".join([f'<span class="{config["class"]}">{s}</span>' for s in ml_results['skills']])
    
    html = html.replace("{{NAME}}", "Professional Portfolio")
    html = html.replace("{{BIO}}", ml_results['bio'])
    html = html.replace(config["container"], config["container"] + skills_html)
    
    css_path = os.path.join(TEMPLATES_DIR, theme, "style.css")
    with open(css_path, "r") as f:
        css = f.read()
    css = css.replace("{{COLOR}}", primary_color)
    
    with open(os.path.join(user_dir, "index.html"), "w") as f:
        f.write(html)
    with open(os.path.join(user_dir, "style.css"), "w") as f:
        f.write(css)
    
    zip_path = f"{user_dir}.zip"
    with zipfile.ZipFile(zip_path, 'w') as zipf:
        zipf.write(os.path.join(user_dir, "index.html"), "index.html")
        zipf.write(os.path.join(user_dir, "style.css"), "style.css")

    return {"preview_url": f"/preview/{job_id}", "job_id": job_id}

# ... (rest of the preview/download endpoints remain the same) [cite: 1]
if __name__ == "__main__":
    import uvicorn
    # Change port from 8000 to 8080
    uvicorn.run(app, host="127.0.0.1", port=8000)