from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from openai import OpenAI
import os
import uvicorn

# API key Groq
client = OpenAI(
    api_key="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",
    base_url="https://api.groq.com/openai/v1"
)

app = FastAPI()

# cho phép web chat gọi API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Message(BaseModel):
    message: str

# route test để Railway kiểm tra server
@app.get("/")
def root():
    return {"status": "SiggyNine AI Bot is running"}

@app.post("/chat")
def chat(msg: Message):

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {
                "role": "system",
                "content": "You are a helpful crypto AI assistant. Answer questions about Bitcoin, Ethereum, trading, and blockchain."
            },
            {
                "role": "user",
                "content": msg.message
            }
        ]
    )

    return {
        "reply": response.choices[0].message.content
    }


# chạy server cho Railway
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    uvicorn.run(app, host="0.0.0.0", port=port)