from flask import Flask, request, jsonify
from flask_cors import CORS
import pytesseract
import PyPDF2
from transformers import pipeline
from googleapiclient.discovery import build

# Set up Flask app
app = Flask(__name__)
CORS(app)

# Hugging Face Zero-shot Classification Pipeline
classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")

# YouTube API key
YOUTUBE_API_KEY = "YOUR_YOUTUBE_API_KEY"

# Function to extract text from a PDF file
def extract_text_from_pdf(file_path):
    with open(file_path, 'rb') as pdf_file:
        reader = PyPDF2.PdfReader(pdf_file)
        return " ".join(page.extract_text() for page in reader.pages)

# Detect role using zero-shot classification
def detect_role(text):
    roles = ["Data Scientist", "Software Engineer", "Project Manager", "Business Analyst", "Unknown"]
    result = classifier(text, roles)
    return result["labels"][0]

# Fetch YouTube videos for a job role
def fetch_youtube_videos(query):
    youtube = build("youtube", "v3", developerKey=YOUTUBE_API_KEY)
    search_response = youtube.search().list(
        q=query, part="snippet", maxResults=5, type="video"
    ).execute()
    return [
        {"title": item["snippet"]["title"], "url": f"https://www.youtube.com/watch?v={item['id']['videoId']}"}
        for item in search_response["items"]
    ]

@app.route('/upload', methods=['POST'])
def upload_resume():
    if 'file' not in request.files:
        return jsonify({"error": "No file provided"}), 400
    file = request.files['file']
    file_path = f"./uploads/{file.filename}"
    file.save(file_path)
    
    # Extract text from the uploaded resume
    text = extract_text_from_pdf(file_path)
    role = detect_role(text)
    
    # If the role is "Unknown", fetch YouTube videos for career guidance
    if role.lower() == "unknown":
        videos = fetch_youtube_videos("career guidance")
    else:
        videos = fetch_youtube_videos(role)
    
    return jsonify({"role": role, "videos": videos})

if __name__ == '__main__':
    app.run(debug=True)
