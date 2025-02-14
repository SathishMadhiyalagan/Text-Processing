
# Text Processing Web Application

This is a Flask-based web application for processing text. It provides functionalities such as text summarization, keyword extraction, and sentiment analysis. The processed data is stored in an SQLite database, and the application exposes RESTful APIs for interaction.

## Folder Structure

```
llmEnv/                  # Virtual environment folder (ignored in .gitignore)
app/                     # Main application folder
├── app.py               # Main Flask application file
├── requirements.txt     # Python dependencies
└── instance/            # Folder for SQLite database (ignored in .gitignore)
.gitignore               # Specifies files/folders to ignore in Git
```

## Features

- **Text Summarization**: Uses the BART model from Hugging Face to generate concise summaries.
- **Keyword Extraction**: Utilizes spaCy to extract meaningful keywords from the input text.
- **Sentiment Analysis**: Employs TextBlob to determine the sentiment (Positive, Negative, or Neutral) of the text.
- **Database Storage**: Stores processed text data (original text, summary, keywords, and sentiment) in an SQLite database.
- **RESTful APIs**: Provides endpoints for text processing, retrieving history, and deleting records.

## Setup Instructions

### Prerequisites

- Python 3.8 or higher (I have Python 3.11.0 installed on my machine)
- Pip (Python package manager)

### Steps

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/SathishMadhiyalagan/Text-Processing
   cd Text-Processing
   ```

2. **Set Up a Virtual Environment**:
   ```bash
   python -m venv llmEnv
   ```

3. **Activate the Virtual Environment**:
   - On Windows:
     ```bash
     llmEnv\Scripts\activate
     ```
   - On macOS/Linux:
     ```bash
     source llmEnv/bin/activate
     ```

4. **Install Dependencies**:
   Navigate to the `app` folder and install the required packages:
   ```bash
   cd app
   pip install -r requirements.txt
   ```

5. **Run the Application**:
   Start the Flask development server:
   ```bash
   python app.py
   ```
   The first time you run this command, it may take some time to download the required models, depending on your internet speed and system configuration. Once the download is complete, restarting your server in the future will take less time.
   
   The application will be available at `http://127.0.0.1:5000`.

6. **Access the Application**:
   - Open your browser and navigate to `http://127.0.0.1:5000`.
   - Use the provided APIs to interact with the application.

## API Endpoints

- **GET `/`**: Renders the main HTML page (if a frontend is implemented).
- **POST `/process`**: Processes the input text and returns the summary, keywords, and sentiment.
  - Request Body:
    ```json
    {
      "text": "Your input text here"
    }
    ```
  - Response:
    ```json
    {
      "text": "Your input text here",
      "summary": "Generated summary",
      "keywords": ["list", "of", "keywords"],
      "sentiment": "Positive/Negative/Neutral"
    }
    ```

- **GET `/history`**: Retrieves all processed text records from the database.
  - Response:
    ```json
    [
      {
        "id": 1,
        "text": "Original text",
        "summary": "Generated summary",
        "keywords": ["list", "of", "keywords"],
        "sentiment": "Positive/Negative/Neutral"
      },,,,
      
    ]
    ```

## Dependencies

The required Python packages are listed in `requirements.txt`. They include:
- Flask
- Flask-SQLAlchemy
- google-generativeai
- spacy
- textblob
- transformers

## .gitignore

The `.gitignore` file ensures that the following files/folders are not tracked by Git:
- `llmEnv/` (virtual environment)
- `app/instance/` (SQLite database folder)

## Contributing

If you'd like to contribute to this project, please follow these steps:
1. Fork the repository.
2. Create a new branch for your feature or bugfix.
3. Commit your changes.
4. Submit a pull request.



### Key Updates:
1. **Folder Structure**:
   - The `.gitignore` file is now outside the `app` folder.
   - The `llmEnv` folder (virtual environment) is now included in the `.gitignore`.

2. **Setup Instructions**:
   - Updated the virtual environment name to `llmEnv` to match your setup.

3. **.gitignore Section**:
   - Added `llmEnv/` and `app/instance/` to the list of ignored files/folders.

This `README.md` now accurately reflects your project structure and setup. Let me know if you need further adjustments!