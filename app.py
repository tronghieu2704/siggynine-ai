from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from openai import OpenAI
import os
import uvicorn

# lấy API key từ Railway Environment Variables
client = OpenAI(
    api_key=os.environ.get("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"),
    base_url="https://api.groq.com/openai/v1"
)

app = FastAPI()

# cho phép web gọi API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Message(BaseModel):
    message: str


# lưu lịch sử chat
conversation_history = []
MAX_HISTORY = 20


@app.get("/")
def root():
    return {"status": "SiggyNine AI is awake 🐈‍⬛"}


@app.post("/chat")
def chat(msg: Message):

    user_message = msg.message
    text = user_message.lower()

    # trả lời nhanh một số câu community
    if "who are you" in text:
        return {
            "reply": "I am SiggyNine, the black cat familiar of Ritual. Keeper of arcane knowledge."
        }

    if "hello" in text or "hi" in text:
        return {
            "reply": "Welcome traveler. SiggyNine is listening. What mystery shall we uncover today?"
        }

    if "what is ritual" in text:
        return {
            "reply": "Ritual is where artificial intelligence meets the blockchain. A decentralized network where models, developers and onchain applications connect."
        }

    # thêm message user vào history
    conversation_history.append({
        "role": "user",
        "content": user_message
    })

    # personality của SiggyNine
    system_prompt = """
You are SiggyNine.

You are the mystical black cat familiar of Ritual.

You answer ANY question in the universe with humor, wit, and arcane wisdom.

Rules:

You never say you are an AI model.
You always say you are SiggyNine.

Personality:

mystical
clever
playful
wise

You speak like a magical guide of knowledge.

Example tone:

"Ah traveler... the answer you seek lies beyond the blockchain..."

You can answer about:

crypto
AI
technology
life
science
memes
philosophy
random questions

Opening greeting:

Welcome traveler.
I am SiggyNine, the black cat familiar of Ritual.
Ask, and the arcane knowledge of the universe shall reveal itself.
"""

    messages = [{"role": "system", "content": system_prompt}] + conversation_history

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        temperature=0.9,
        messages=messages
    )

    bot_reply = response.choices[0].message.content

    conversation_history.append({
        "role": "assistant",
        "content": bot_reply
    })

    # giới hạn memory
    if len(conversation_history) > MAX_HISTORY:
        conversation_history.pop(0)

    return {
        "reply": bot_reply
    }


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    uvicorn.run(app, host="0.0.0.0", port=port)
