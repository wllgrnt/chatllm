import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from pydantic import BaseModel
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Initialize OpenAI with API key
# openai.api_key = os.getenv("OPENAI_API_KEY")
openai_model = os.getenv("OPENAI_MODEL")
openai_client = OpenAI(
    api_key = os.getenv("OPENAI_API_KEY")
)
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins, but you can restrict this for production
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods (POST, GET, etc.)
    allow_headers=["*"],  # Allows all headers
)


class MessageRequest(BaseModel):
    message: str
    history: list

@app.post("/chat")
async def chat_with_gpt(request: MessageRequest):
    # Extract user message and conversation history
    user_message = request.message
    message_history = request.history or [{"role": "system", "content": "You are a helpful assistant."}]

    # Add the user message to the conversation history
    message_history.append({"role": "user", "content": user_message})

    # Call the OpenAI API
    try:
        response = openai_client.chat.completions.create(
            model=openai_model,
            messages=message_history
        )
        print(response)
        assistant_message = response.choices[0].message.content

        # Append the assistant message to the history (if needed for future context)
        # message_history.append({"role": "assistant", "content": assistant_message})

        return {"assistant_message": assistant_message}
    except Exception as e:
        return {"error": str(e)}