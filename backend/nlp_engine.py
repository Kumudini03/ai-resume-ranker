import fitz  # PyMuPDF
from sentence_transformers import SentenceTransformer, util

# Load the AI model
model = SentenceTransformer('all-MiniLM-L6-v2')

def extract_text_from_pdf(pdf_path):
    text = ""
    try:
        doc = fitz.open(pdf_path)
        for page in doc:
            text += page.get_text()
    except Exception as e:
        print(f"Error reading PDF: {e}")
    return text

def calculate_score(job_description, resume_text):
    embeddings = model.encode([job_description, resume_text])
    score = util.cos_sim(embeddings[0], embeddings[1])
    return round(float(score) * 100, 2)