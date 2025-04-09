from fastapi import FastAPI, HTTPException, Request, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
from groq import Groq
from dotenv import load_dotenv 
import os
from .auth import get_and_validate_current_user

load_dotenv()

GROQ_API_KEY = os.environ.get("GROQ_API_KEY")

if not GROQ_API_KEY:
    raise RuntimeError("GROQ_API_KEY is not set. Set it in .env file.")
client = Groq(api_key=GROQ_API_KEY)

app = FastAPI()

auth_scheme  = HTTPBearer()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://www.foliofusion.art"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class TextRequest(BaseModel):
    text: str

class HealthCheck(BaseModel):
    status: str = "OK"

@app.get("/health", tags=["healthcheck"], summary="Perform a health check",)
async def health_check():
    """
    Endpoint to perform a health check on.
    """
    return HealthCheck(status="OK")

@app.post("/enhance-text", summary="AI endpoints",)
async def enhance_text(request: Request, body: TextRequest, credentials: HTTPAuthorizationCredentials = Depends(auth_scheme)):
    """
    Enhance the grammar and clarity of the given text using professional IT language.
    """
    auth_header = request.headers.get("authorization")
    get_and_validate_current_user(auth_header)
    
    user_input = body.text
    if len(user_input.split()) > 100:
        raise HTTPException(status_code=400, detail="Input text exceeds the maximum limit of 100 words.")
   
    try:
        conversation = client.chat.completions.create(
            messages=[  
                {
                    "role": "system",
                    "content": "You are a helpful assistant that improves grammar and clarity. Provide a concise and professional rewrite of the user's input without explanations or additional commentary.",
                },
                {
                    "role": "user",
                    "content": user_input,
                }
            ],
            model="llama-3.1-8b-instant",
            max_completion_tokens=500,
            temperature=0.8, # more creative
        )
        generated_text = conversation.choices[0].message.content
        print(generated_text)
        return {
            "original": user_input,
            "enhanced": generated_text,
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))