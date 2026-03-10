from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from openai import OpenAI
from gtts import gTTS
import requests
import uvicorn
import uuid

# ====== GROQ API ======
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

# ===== MEMORY STORE =====
chat_memory = {}

class Message(BaseModel):
    message: str
    user_id: str = "default"


@app.get("/")
def root():
    return {"status": "SiggyNine AI Bot is running"}


# ===== INTERNET SEARCH =====
def search_web(query):

    url = "https://api.duckduckgo.com/"
    params = {
        "q": query,
        "format": "json"
    }

    try:
        res = requests.get(url, params=params).json()
        return res.get("AbstractText", "")
    except:
        return ""


# ===== CHAT ROUTE =====
@app.post("/chat")
def chat(msg: Message):

    user_id = msg.user_id

    if user_id not in chat_memory:
        chat_memory[user_id] = []

    memory = chat_memory[user_id]

    # tìm thông tin internet
    web_info = search_web(msg.message)

    system_prompt = f"""
You are SiggyNine, the mystical black cat familiar of Ritual.

You possess knowledge about everything in the universe.

You can speak ALL languages.

Always answer in the user's language.

You have access to real-time information from the internet:

{web_info}

Personality:
playful, witty, mystical, sarcastic black cat.

You NEVER say you are an AI.
You ALWAYS say you are SiggyNine.

Opening line:

Welcome, traveler.
I am SiggyNine, the black cat familiar of Ritual.
Ask, and the arcane knowledge of the universe shall reveal itself.
"""

    messages = [{"role": "system", "content": system_prompt}]

    messages += memory[-10:]

    messages.append({"role": "user", "content": msg.message})

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        temperature=0.9,
        top_p=0.95,
        messages=messages
    )

    reply = response.choices[0].message.content

    # lưu memory
    memory.append({"role": "user", "content": msg.message})
    memory.append({"role": "assistant", "content": reply})

    # ===== TEXT TO SPEECH =====
    filename = f"voice_{uuid.uuid4()}.mp3"

    tts = gTTS(reply)
    tts.save(filename)

    return {
        "reply": reply,
        "voice": filename
    }


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)
