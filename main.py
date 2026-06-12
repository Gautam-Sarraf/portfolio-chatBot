from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
from util import ask_portfolio_bot


app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class ChatMessage(BaseModel):
    role: str
    content: str


class ChatRequest(BaseModel):
    message: str
    chat_history: List[ChatMessage] = []


class ChatResponse(BaseModel):
    response: str


@app.get("/")
def home():
    return {
        "message":
        "Portfolio Chatbot API Running"
    }


@app.post(
    "/chat",
    response_model=ChatResponse
)
def chat(
    request: ChatRequest
):

    history = [
        {
            "role": msg.role,
            "content": msg.content
        }
        for msg in request.chat_history
    ]

    response = ask_portfolio_bot(
        question=request.message,
        chat_history=history
    )

    return {
        "response": response
    }