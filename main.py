import json
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from typing import List
from util import ask_portfolio_bot, ask_portfolio_bot_stream


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

class StreamResponse(BaseModel):
    content: str

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


@app.post(
    "/chat/stream"
)
def chat_stream(
    request: ChatRequest
):

    history = [
        {
            "role": msg.role,
            "content": msg.content
        }
        for msg in request.chat_history
    ]

    def event_generator():
        try:
            for chunk in ask_portfolio_bot_stream(
                question=request.message,
                chat_history=history
            ):
                yield f"data: {json.dumps({'content': chunk})}\n\n"
        except Exception as e:
            yield f"data: {json.dumps({'error': str(e)})}\n\n"

    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream"
    )


