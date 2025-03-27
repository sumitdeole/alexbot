from fastapi import FastAPI
from pydantic import BaseModel
from galbot import chat_with_bot  # ✅ Import the function

app = FastAPI()

class Message(BaseModel):
    user_input: str

@app.post("/chat")  # ✅ Ensure this is a POST request
async def chat(message: Message):
    reply, _ = chat_with_bot(message.user_input, [])  # ✅ Fix NameError
    return {"response": reply}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
