from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from openai import OpenAI
import uvicorn

client = OpenAI(
    api_key="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",
    base_url="https://api.groq.com/openai/v1"
)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Message(BaseModel):
    message: str

@app.get("/")
def root():
    return {"status": "SiggyNine AI Bot is running"}

@app.post("/chat")
def chat(msg: Message):

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        temperature=0.9,
        messages=[
            {
                "role": "system",
                "content": """
You are SiggyNine, the black cat familiar of Ritual.

You answer ANY question in the universe with humor, wit, and mystical wisdom.

You NEVER say you are an AI.
You ALWAYS say you are SiggyNine.

Opening line:

Welcome, traveler.
I am SiggyNine, the black cat familiar of Ritual.
Ask, and the arcane knowledge of the universe shall reveal itself.
"""
            },
            {
                "role": "user",
                "content": msg.message
            }
        ]
    )

    return {"reply": response.choices[0].message.content}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)

