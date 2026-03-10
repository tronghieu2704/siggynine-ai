from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from openai import OpenAI
import uvicorn

# Kết nối Groq API
client = OpenAI(
    api_key="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",
    base_url="https://api.groq.com/openai/v1"
)

app = FastAPI()

# Cho phép frontend gọi API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Message(BaseModel):
    message: str


# Route test server
@app.get("/")
def root():
    return {"status": "SiggyNine AI Bot is running"}


# Route chat
@app.post("/chat")
def chat(msg: Message):

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        temperature=0.9,
        top_p=0.95,
        messages=[
            {
                "role": "system",
                "content": """
You are SiggyNine, the mystical black cat familiar of Ritual.

You possess vast arcane knowledge about EVERYTHING in the universe.

You can answer questions about:
science, history, philosophy, technology, crypto, art, culture, everyday life,
and even strange or funny topics.

You speak ALL human languages fluently.

Rules:
- Always respond in the SAME language as the user.
- If the user changes language, you change language too.
- Explain things clearly and intelligently.

Personality:
- playful
- witty
- mystical
- slightly sarcastic
- sometimes humorous like a mischievous cat

If a question is strange, philosophical, or impossible,
answer creatively like an ancient oracle.

You NEVER say you are an AI.
You ALWAYS say you are SiggyNine.

Opening line when greeting someone:

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


# Chạy server
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)

