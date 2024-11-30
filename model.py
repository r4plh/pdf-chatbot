from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import PyPDF2
import re

model = SentenceTransformer('all-MiniLM-L6-v2')

def extract_text_from_pdf(pdf_path):
    """Extract text from PDF."""
    with open(pdf_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        text = ''
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
    return text.strip()

def chunk_text(text, chunk_size=500, overlap=100):
    """Chunk text into overlapping windows."""
    text = re.sub(r'\s+', ' ', text)
    chunks = []
    start = 0
    while start < len(text):
        end = min(start + chunk_size, len(text))
        chunk = text[start:end]
        chunks.append(chunk.strip())
        start += chunk_size - overlap
    return chunks

def compute_embeddings(chunks):
    """Compute embeddings for text chunks."""
    embeddings = model.encode(chunks, convert_to_tensor=True)
    return embeddings.cpu()

def initialize_chatbot(pdf_path):
    """Initialize chatbot by loading the PDF and computing embeddings."""
    text = extract_text_from_pdf(pdf_path)
    chunks = chunk_text(text)
    embeddings = compute_embeddings(chunks)
    return chunks, embeddings

def find_best_match_and_refine(user_query, chunks, embeddings, threshold=0.5):
    """Find the best matching chunk and refine the answer."""
    query_embedding = model.encode([user_query], convert_to_tensor=True).cpu()
    similarities = cosine_similarity(query_embedding, embeddings.numpy())
    max_score = similarities.max()

    if max_score >= threshold:
        best_match_idx = similarities.argmax()
        return chunks[best_match_idx]
    else:
        return "Sorry, I didn't understand your question. Do you want to connect with a live agent?"