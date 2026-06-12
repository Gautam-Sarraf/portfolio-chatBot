Gautam Sarraf's AI Portfolio Chatbot API
This is a Retrieval-Augmented Generation (RAG) backend API for Gautam Sarraf's Portfolio. It allows users to ask questions about Gautam's skills, experience, and projects in natural language, retrieving relevant context and generating accurate, professional responses via Google's Gemini models.

Features
FastAPI Backend: A lightweight, high-performance, and asynchronous API wrapper.
Simple RAG (Retrieval-Augmented Generation) Pipeline:
Parses and chunks Gautam's professional profile (doc/gautam_sarraf_info.txt).
Embeds chunks using Google's modern gemini-embedding-2 model.
Employs NumPy for calculating cosine similarity to retrieve the most contextually relevant chunks.
Gemini 2.5 Flash Integration: Generates concise, professional, persona-driven answers based exclusively on the retrieved context.
Conversation History Support: Retains chat history context within the API request for continuous conversations.
CORS Configured: Preloaded with CORS middleware to allow requests from any frontend port/origin.
Tech Stack
Framework: FastAPI
Data Validation: Pydantic v2
Mathematical Operations: NumPy
LLM/SDK: Google GenAI SDK
ASGI Web Server: Uvicorn


Project Structure


├── doc/
│   └── gautam_sarraf_info.txt  # Gautam's profile & knowledge base
├── main.py                     # FastAPI server & route handlers
├── util.py                     # RAG pipeline: chunking, embedding, similarity search, & LLM call
├── requirements.txt            # Python dependencies
├── .gitignore                  # Git ignore rules (excludes .env and __pycache__)
└── .env                        # Local environment secrets (ignored by Git)
Setup & Installation
1. Clone & Navigate
bash
git clone https://github.com/Gautam-Sarraf/portfolio-chatBot.git
cd portfolio-chatBot
2. Install Dependencies
Ensure you have Python 3.10+ installed, then run:

bash
pip install -r requirements.txt
3. Environment Variable Configuration
Create a .env file in the root of the project:

env
GEMINI_API_KEY=your_actual_gemini_api_key_here
(Note: .env is already configured in .gitignore to prevent secret leaks.)

4. Running the Server
Start the local development server with auto-reload enabled:

bash
uvicorn main:app --reload
The API will be available at http://127.0.0.1:8000.

API Endpoints
1. Home Health Check
Verify if the API service is up and running.

URL: /
Method: GET
Response:
json
{
  "message": "Portfolio Chatbot API Running"
}
2. Chat Endpoint
Submit a question along with optional conversation history to receive an AI-generated answer.

URL: /chat

Method: POST

Content-Type: application/json

Request Body Schema:

json
{
  "message": "What programming languages does Gautam know?",
  "chat_history": [
    {
      "role": "user",
      "content": "Hi, who are you?"
    },
    {
      "role": "model",
      "content": "I am Gautam Sarraf's AI Portfolio Assistant. How can I help you?"
    }
  ]
}
(Note: chat_history defaults to an empty list [] if omitted.)

Response Body Schema:

json
{
  "response": "Gautam is highly proficient in Python (his principal backend language), TypeScript, and JavaScript (ES6+)."
}
3:15 PM
