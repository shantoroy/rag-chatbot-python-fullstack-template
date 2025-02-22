import chainlit as cl
import requests
import os

@cl.on_chat_start
async def start():
    """Initialize the chat session."""
    api_url = os.getenv("BACKEND_URL", "http://localhost:8000")
    cl.user_session.set("api_url", api_url)

    await cl.Message(
        content="👋 Hello! I'm your company knowledge assistant. Ask me anything!",
        author="Assistant"
    ).send()

@cl.on_message
async def main(message: cl.Message):
    """Handle incoming chat messages."""
    api_url = cl.user_session.get("api_url")

    try:
        response = requests.post(
            f"{api_url}/ask",
            json={"text": message.content}
        )
        response.raise_for_status()
        result = response.json()

        if result.get("status") == "success":
            answer = result.get("answer", "I'm not sure how to respond to that.")
        else:
            answer = f"Error: {result.get('error', 'Unknown error')}"

    except Exception as e:
        answer = f"❌ Sorry, an error occurred: {str(e)}"

    await cl.Message(
        content=answer,
        author="Assistant"
    ).send()
