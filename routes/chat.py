from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel
from typing import List
from services.openrouter import get_chat_response
from services.rate_limiter import rate_limiter

router = APIRouter()


class Message(BaseModel):
    role: str
    content: str


class ChatRequest(BaseModel):
    messages: List[Message]


class ChatResponse(BaseModel):
    message: str


@router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest, req: Request):
    # Get IP address
    ip = req.client.host

    # Check rate limit
    allowed, minutes = rate_limiter.is_allowed(ip)
    if not allowed:
        raise HTTPException(
            status_code=429,
            detail=f"Rate limit exceeded. Please try again in {minutes} minutes."
        )

    try:
        # Get response from OpenRouter
        messages = [{"role": m.role, "content": m.content}
                    for m in request.messages]
        response = await get_chat_response(messages)

        return ChatResponse(message=response)
    except Exception as e:
        raise HTTPException(
            status_code=500, detail="Failed to process request")
