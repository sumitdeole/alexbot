from fastapi import FastAPI
from pydantic import BaseModel
from galbot import chat_with_bot  # ✅ Import the function

app = FastAPI()

# Root route
@app.get("/")  # This will respond with a friendly message at the root URL
async def read_root():
    return {"message": "Hello, welcome to Alexbot! Type something at /chat to interact with the bot."}

class Message(BaseModel):
    user_input: str

# /chat route to handle POST requests and interact with the chatbot
@app.post("/chat")  # ✅ Ensure this is a POST request
async def chat(message: Message):
    # Call chat_with_bot function to get a response from the bot
    reply, _ = chat_with_bot(message.user_input, [])  # ✅ Fix NameError
    return {"response": reply}

# If you want to run it locally
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)  # When deploying, this line can be skipped
