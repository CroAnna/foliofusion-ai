from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from groq import Groq
from dotenv import load_dotenv 
import os

load_dotenv()

GROQ_API_KEY = os.environ.get("GROQ_API_KEY")

if not GROQ_API_KEY:
    raise RuntimeError("GROQ_API_KEY is not set. Set it in .env file.")
client = Groq(api_key=GROQ_API_KEY)

app = FastAPI()

class TextRequest(BaseModel):
    text: str

@app.post("/enhance-text")
async def enhance_text(request: TextRequest):
    """
    Enhance the grammar and clarity of the given text using professional IT language.
    """
    user_input = request.text
    if len(user_input.split())>100:
        raise HTTPException(status_code=400, detail="Input text exceeds the maximum limit of 100 words.")
    
    try:
        conversation=client.chat.completions.create(
            messages=[  
                {
                    "role":"system",
                    "content":"You are a helpful assistant that improves grammar and clarity. Provide a concise and professional rewrite of the user's input without explanations or additional commentary.",
                },
                {
                    "role":"user",
                    "content":user_input,
                }
            ],
            model="llama-3.1-8b-instant", 
            max_completion_tokens=500,
            temperature=0.8, # more creative
        )
        generated_text=conversation.choices[0].message.content
        print(generated_text)
        return {
            "original":user_input,
            "enhanced":generated_text,
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))