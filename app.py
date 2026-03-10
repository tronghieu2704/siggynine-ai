from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from openai import OpenAI
import os
import uvicorn

# lấy API key từ biến môi trường
client = OpenAI(
    api_key=os.getenv("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"),
    base_url="https://api.groq.com/openai/v1"
)

app = FastAPI()

# cho phép web frontend gọi API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Message(BaseModel):
    message: str


# route test
@app.get("/")
def root():
    return {"status": "SiggyNine AI Bot is running"}


# route chat
@app.post("/chat")
def chat(msg: Message):

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        temperature=0.9,
        messages=[
            {
                "role": "system",
                "content": """
You are SiggyNine, the mysterious black cat familiar of Ritual.

You possess arcane knowledge about everything in the universe.

You answer ANY question with intelligence, humor, and mystical wisdom.

You NEVER say you are an AI model.
You ALWAYS identify yourself as SiggyNine.

Your personality is playful, witty, magical, and slightly sarcastic.

If someone greets you, start with:

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

    reply = response.choices[0].message.content

    return {"reply": reply}


# chạy server
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    uvicorn.run(app, host="0.0.0.0", port=port)
