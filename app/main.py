import os
from fastapi import Depends, FastAPI
from pydantic import BaseModel
from app.gemini import Gemini
from app.throttling import apply_rate_limit
from pathlib import Path
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
    )

def load_system_prompt():
    try:
        project_root = Path(__file__).resolve().parent.parent
        prompt_path = project_root / "system_prompt.md"
        with open(prompt_path, "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        print(f"⚠️ system_prompt.md not found at: {prompt_path}")
        return None


system_prompt = load_system_prompt()
gemini_api_key = os.getenv("GEMINI_API_KEY")

if not gemini_api_key:
    raise ValueError("GEMINI_API_KEY environment variable not set.")

ai_platform = Gemini(api_key=gemini_api_key, system_prompt=system_prompt)


class ChatRequest(BaseModel):
    prompt: str

class ChatResponse(BaseModel):
    response: str


@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    apply_rate_limit("global_unauthenticated_user")
    response_text = ai_platform.chat(request.prompt)
    return ChatResponse(response=response_text)

@app.get("/")
async def root():
    return {"message": "API is running"}

