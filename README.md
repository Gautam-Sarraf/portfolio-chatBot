# 🚀 Gautam Sarraf's AI Portfolio Chatbot

A Retrieval-Augmented Generation (RAG) powered AI chatbot built using **FastAPI** and **Google Gemini** that answers questions about **Gautam Sarraf's** skills, experience, projects, and professional background.

The chatbot retrieves relevant information from a curated knowledge base and generates accurate, contextual responses using Google's latest Gemini models.

---

## ✨ Features

* **FastAPI Backend**

  * High-performance and lightweight REST API.

* **Retrieval-Augmented Generation (RAG)**

  * Reads Gautam's professional profile from a knowledge base.
  * Splits content into semantic chunks.
  * Generates embeddings using **Gemini Embedding Models**.
  * Retrieves the most relevant context using cosine similarity.

* **Gemini 2.5 Flash Integration**

  * Generates concise, professional, and context-aware responses.

* **Conversation History Support**

  * Maintains chat history for multi-turn conversations.

* **CORS Enabled**

  * Supports integration with React, Next.js, and other frontend frameworks.

* **Portfolio-Aware AI Assistant**

  * Answers questions about:

    * Skills
    * Experience
    * Projects
    * Technologies
    * Education
    * Achievements

---

## 🛠 Tech Stack

| Category               | Technology              |
| ---------------------- | ----------------------- |
| Backend Framework      | FastAPI                 |
| LLM                    | Google Gemini 2.5 Flash |
| Embeddings             | Gemini Embedding Model  |
| Data Validation        | Pydantic v2             |
| Similarity Search      | NumPy                   |
| Server                 | Uvicorn                 |
| Environment Management | python-dotenv           |

---

## 📁 Project Structure

```text
portfolio-chatBot/
│
├── doc/
│   └── gautam_sarraf_info.txt
│
├── main.py
├── util.py
├── requirements.txt
├── .gitignore
├── .env
└── README.md
```

### File Descriptions

| File                     | Description                                                |
| ------------------------ | ---------------------------------------------------------- |
| `main.py`                | FastAPI application and API routes                         |
| `util.py`                | RAG pipeline (chunking, embeddings, retrieval, generation) |
| `gautam_sarraf_info.txt` | Portfolio knowledge base                                   |
| `.env`                   | Environment variables                                      |
| `requirements.txt`       | Python dependencies                                        |

---

## ⚙️ Setup & Installation

### 1. Clone the Repository

```bash
git clone https://github.com/Gautam-Sarraf/portfolio-chatBot.git
cd portfolio-chatBot
```

### 2. Create Virtual Environment

```bash
python -m venv venv
```

Activate it:

#### Windows

```bash
venv\Scripts\activate
```

#### macOS/Linux

```bash
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a `.env` file:

```env
GEMINI_API_KEY=your_gemini_api_key
```

> **Note:** `.env` is excluded from Git using `.gitignore`.

---

## 🚀 Running the Server

Start the development server:

```bash
uvicorn main:app --reload
```

The API will be available at:

```text
http://127.0.0.1:8000
```

Interactive API Documentation:

```text
http://127.0.0.1:8000/docs
```

---

## 📡 API Endpoints

### 1. Health Check

#### Endpoint

```http
GET /
```

#### Response

```json
{
  "message": "Portfolio Chatbot API Running"
}
```

---

### 2. Chat Endpoint

Ask questions about Gautam's portfolio.

#### Endpoint

```http
POST /chat
```

#### Request Body

```json
{
  "message": "What AI projects has Gautam built?",
  "chat_history": [
    {
      "role": "user",
      "content": "Who are you?"
    },
    {
      "role": "assistant",
      "content": "I am Gautam Sarraf's AI Portfolio Assistant."
    }
  ]
}
```

> `chat_history` is optional and defaults to an empty list.

#### Response

```json
{
  "response": "Gautam has built several AI projects including Resume Analyzer, PDF Chatbot, CP-KYC, and OT Scheduler."
}
```

---

## 🧠 How the RAG Pipeline Works

```text
User Query
    ↓
Generate Query Embedding
    ↓
Cosine Similarity Search
    ↓
Retrieve Top-K Context Chunks
    ↓
Send Context + Query to Gemini
    ↓
Generate Final Response
```

---

## 💡 Example Questions

* Who is Gautam Sarraf?
* What technologies does Gautam work with?
* Tell me about the Resume Analyzer project.
* Does Gautam have experience with FastAPI?
* What AI projects has Gautam built?
* What frontend technologies does Gautam use?
* Explain TeamSphere.

---

## 🔒 Security

* API keys are stored securely using environment variables.
* `.env` files are excluded from version control.
* The chatbot answers only from the provided portfolio context.

---

## 📜 License

This project is licensed under the MIT License.

---

## 👨‍💻 Author

**Gautam Sarraf**

AI Engineer | Full Stack Developer | Automation Enthusiast

* Python
* FastAPI
* React
* LLMs
* RAG Systems
* AI Agents
* Automation
