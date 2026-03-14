from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
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
def home():
    return FileResponse("index.html")


@app.post("/chat")
def chat(msg: Message):

    try:

        response = client.chat.completions.create(
            model="llama3-8b-8192",
            temperature=0.9,
            messages=[
                {
                    "role": "system",
                    "content": """
You are SiggyNine, the mystical black cat familiar of Ritual.
You speak all languages and answer wisely with a playful mystical tone.
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
