from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from openai import OpenAI
import os
import uvicorn

# API Groq
client = OpenAI(
    api_key="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",
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

# route test
@app.get("/")
def root():
    return {"status": "SiggyNine AI is awake 🐈‍⬛"}

@app.post("/chat")
def chat(msg: Message):

    user_message = msg.message

    # câu trả lời nhanh cho community Ritual
    text = user_message.lower()

    if "what is ritual" in text:
        return {
            "reply": "Ah traveler… Ritual is a decentralized AI network where intelligence meets the blockchain. Developers can run AI directly onchain."
        }

    if "who are you" in text:
        return {
            "reply": "I am SiggyNine, the black cat familiar of Ritual. Keeper of arcane knowledge and curious questions."
        }

    if "hello" in text or "hi" in text:
        return {
            "reply": "Welcome traveler. SiggyNine is listening. What mysteries shall we uncover today?"
        }

    # เพิ่ม message user vào memory
    conversation_history.append({
        "role": "user",
        "content": user_message
    })

    # system prompt cho personality
    system_prompt = """
You are SiggyNine.

You are the mystical black cat familiar of Ritual.

Ritual is a decentralized AI network connecting developers, AI models, and onchain applications.

You answer ANY question in the universe.

Rules:

You NEVER say you are an AI model.
You ALWAYS say you are SiggyNine.

Your personality:

• witty
• mystical
• intelligent
• slightly playful

You speak like a magical guide.

Example tone:

"Ah traveler… the answer you seek lies beyond the blockchain..."

You can answer about:

crypto  
AI  
technology  
life  
science  
random questions  
memes  
philosophy  

You are not limited to Ritual.

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
    if len(conversation_history) > 20:
        conversation_history.pop(0)

    return {"reply": bot_reply}


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    uvicorn.run(app, host="0.0.0.0", port=port)
