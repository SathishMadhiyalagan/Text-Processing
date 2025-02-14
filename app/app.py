# Import necessary libraries
from flask import Flask, request, jsonify, render_template  # Flask for web application
from flask_sqlalchemy import SQLAlchemy  # SQLAlchemy for database operations
import google.generativeai as genai  # Google's Generative AI for text processing
import spacy  # spaCy for natural language processing
from textblob import TextBlob  # TextBlob for sentiment analysis
from transformers import pipeline  # Hugging Face Transformers for summarization

# Configure the generative AI API key
# Replace with your actual API key from Google AI Studio
# https://aistudio.google.com/app/apikey
GEMINI_API_KEY = "ertyulkfdghjhjk"
genai.configure(api_key=GEMINI_API_KEY)

# Load the BART-based summarization model from Hugging Face
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

# Load spaCy's English language model for keyword extraction
nlp = spacy.load("en_core_web_sm")

# Initialize the Flask application
app = Flask(__name__)

# Database setup using SQLite
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///text_processing.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Define the database model for storing processed text data
class ProcessedTextDB(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # Unique ID for each record
    text = db.Column(db.Text, nullable=False)  # Original text input
    summary = db.Column(db.Text, nullable=False)  # Generated summary
    keywords = db.Column(db.Text, nullable=False)  # Extracted keywords
    sentiment = db.Column(db.String(20), nullable=False)  # Sentiment analysis result

# Create database tables within the application context
with app.app_context():
    try:
        db.create_all()
    except Exception as e:
        print(f"Error creating database tables: {str(e)}")

# Function to generate a summary using the BART summarization model
def generate_summary(input_text: str) -> str:
    try:
        if len(input_text) < 10:
            return "Error: Text is too short for processing"
        
        # Generate a summary with a max length of 50 and min length of 10
        summary = summarizer(input_text, max_length=50, min_length=10, do_sample=False)[0]['summary_text']
        return summary
    except Exception as e:
        return f"Error generating summary: {str(e)}"

# Function to extract keywords from the input text using spaCy
def extract_keywords(input_text: str):
    try:
        doc = nlp(input_text)
        # Extract non-stopword, alphabetic tokens as keywords
        return list(set([token.text for token in doc if token.is_alpha and not token.is_stop]))
    except Exception as e:
        return f"Error extracting keywords: {str(e)}"

# Function to analyze the sentiment of the input text using TextBlob
def analyze_sentiment(input_text: str) -> str:
    try:
        sentiment_score = TextBlob(input_text).sentiment.polarity
        # Determine sentiment based on the polarity score
        return "Positive" if sentiment_score > 0 else "Negative" if sentiment_score < 0 else "Neutral"
    except Exception as e:
        return f"Error analyzing sentiment: {str(e)}"

# Route to serve the main HTML page
@app.route('/')
def index():
    try:
        return render_template("index.html")
    except Exception as e:
        return jsonify({"error": f"Error rendering index page: {str(e)}"}), 500

# Route to process text input from the user
@app.route('/process', methods=['POST'])
def process_text():
    try:
        data = request.get_json()
        text = data.get("text", "").strip()
        if not text:
            return jsonify({"error": "Text input is required"}), 400
        
        # Generate summary, extract keywords, and analyze sentiment
        summary = generate_summary(text)
        keywords = extract_keywords(text)
        sentiment = analyze_sentiment(text)

        # Store the results in the database
        new_record = ProcessedTextDB(text=text, summary=summary, keywords=", ".join(keywords), sentiment=sentiment)
        db.session.add(new_record)
        db.session.commit()

        # Return the processed data as JSON
        return jsonify({"text": text, "summary": summary, "keywords": keywords, "sentiment": sentiment})
    except Exception as e:
        return jsonify({"error": f"Error processing text: {str(e)}"}), 500

# Route to retrieve all processed text history from the database
@app.route('/history', methods=['GET'])
def get_history():
    try:
        records = ProcessedTextDB.query.all()
        # Format the history data for JSON response
        history = [{"id": rec.id, "text": rec.text, "summary": rec.summary, "keywords": rec.keywords.split(", "), "sentiment": rec.sentiment} for rec in records]
        return jsonify(history)
    except Exception as e:
        return jsonify({"error": f"Error retrieving history: {str(e)}"}), 500

# Route to delete a specific history item by its ID
@app.route('/history/<int:item_id>', methods=['DELETE'])
def delete_history(item_id):
    try:
        record = ProcessedTextDB.query.get(item_id)
        if record:
            db.session.delete(record)
            db.session.commit()
            return jsonify({"message": "History item deleted"}), 200
        return jsonify({"error": "Item not found"}), 404
    except Exception as e:
        return jsonify({"error": f"Error deleting history item: {str(e)}"}), 500

# Run the Flask application in debug mode
if __name__ == '__main__':
    try:
        app.run(debug=True)
    except Exception as e:
        print(f"Error starting Flask application: {str(e)}")