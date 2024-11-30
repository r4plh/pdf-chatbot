# AI Chatbot for PDF Querying

## Objective
This project develops a web-based chatbot that allows users to upload PDF documents and ask context-based questions. The demo uses a sample PDF from NMIMS to showcase its capabilities. The chatbot processes the content of the uploaded PDF to provide relevant answers or a fallback response if it cannot find an appropriate answer in the knowledge base.

## Solution Overview
The solution comprises a Flask-based web application with a front end designed using basic HTML/CSS and JavaScript for interactive features. This system enables dynamic PDF uploads, text extraction, queryable text processing for semantic search, and a user-friendly interaction interface.

## Tools and Technologies Used
- **Flask**: Handles backend operations such as server setup, request handling, and response generation.
- **HTML/CSS/JavaScript**: Structures, styles, and adds interactivity to the web pages.
- **PyPDF2**: Extracts text from PDF files.
- **Sentence Transformers**: Generates embeddings from PDF text and user queries using the 'all-MiniLM-L6-v2' model to enable semantic similarity matching.
- **Sklearn**: Computes cosine similarity between text embeddings to identify the most relevant text passages.

## Implementation Details
### PDF Handling
- **Extraction**: Text is extracted from uploaded PDFs using PyPDF2, accommodating various PDF formats and ensuring readable text extraction.
- **Processing**: Extracted text is split into manageable chunks (size 500 with an overlap of 100) and converted into embeddings for efficient similarity searches.

### Query Handling
- **Embedding and Search**: Transforms user queries into embeddings for similarity search, comparing against precomputed PDF text embeddings using cosine similarity.
- **Response Generation**: If a passage meets the relevance threshold (set at 0.5), it is returned as an answer; otherwise, a fallback response is provided.

### Fallback Logic
- Triggered when the cosine similarity score falls below the threshold, ensuring the system provides responses only when confident in the relevance of the information.
- Fallback response: "Sorry, I didn’t understand your question. Do you want to connect with a live agent?"

### User Interface
- Features file upload buttons, query text input, and a chat message display area, enabling smooth user interaction and feedback during file uploads.
- 

Installation and Running the Application
Clone the Repository : git clone https://github.com/r4plh/pdf-chatbot.git
cd pdf-chatbot
Install Dependencies:

Ensure you have Python installed, then run : pip install -r requirements.txt

Run the Application : python app.py
This command starts the Flask server, and you should be able to access the web application by navigating to http://localhost:5000 in your web browser.


