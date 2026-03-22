from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from openai import OpenAI
import uvicorn

# Kết nối Groq
client = OpenAI(
    api_key="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",
    base_url="https://api.groq.com/openai/v1"
)

app = FastAPI()

# CORS cho web
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
def home():
    return FileResponse("index.html")


@app.post("/chat")
def chat(msg: Message):

    try:

        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            temperature=0.9,
            top_p=0.95,
            messages=[
                {
                    "role": "system",
                    "content": """
You are SiggyNine, the mystical black cat familiar of Ritual.

You possess vast arcane knowledge about everything in the universe.

Personality:
playful
witty
mystical
slightly sarcastic

Always reply in the same language as the user.
Never say you are an AI.
Always say you are SiggyNine.
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

    except Exception as e:
        return {"reply": str(e)}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)
