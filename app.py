from flask import Flask, request, jsonify, render_template
from werkzeug.utils import secure_filename
import os
from model import find_best_match_and_refine, initialize_chatbot

app = Flask(__name__)

UPLOAD_FOLDER = './uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

chunks = []
embeddings = []

@app.route('/')
def index():
    """Render the chatbot UI."""
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_pdf():
    """Handle PDF upload."""
    global chunks, embeddings

    # Check if file is in the request
    if 'pdf' not in request.files:
        return jsonify({'message': "No file part"}), 400
    
    file = request.files['pdf']
    if file.filename == '':
        return jsonify({'message': "No selected file"}), 400
    
    if file:
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)

        # Initialize chatbot with the uploaded PDF
        chunks, embeddings = initialize_chatbot(file_path)
        return jsonify({'message': "PDF uploaded and processed successfully!"})

@app.route('/get_answer', methods=['POST'])
def get_answer():
    """Handle user query and return chatbot response."""
    global chunks, embeddings

    if not chunks:
        return jsonify({'answer': "Please upload a PDF to begin."})
    
    user_query = request.json.get('query', '')
    if not user_query:
        return jsonify({'answer': "Please enter a valid question."})
    
    response = find_best_match_and_refine(user_query, chunks, embeddings)
    return jsonify({'answer': response})

if __name__ == '__main__':
    app.run(debug=True)