import chainlit as cl
import requests
import logging
import os

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

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
            sources = result.get("sources", [])  # Get the list of sources
            source_info = ""

            if sources:
                unique_sources = set()  # Use a set to store unique sources
                for source in sources:
                    unique_sources.add(source.get('source', 'Unknown Source'))

                source_info = "\n\n**Sources:**\n"  # Add a separator and heading
                for unique_source in unique_sources:
                    source_info += f"- {unique_source}\n"
            else:
                source_info = "\n\nNo relevant documents were found."

            full_answer = answer + source_info  # Combine answer and sources
        else:
            full_answer = f"❌ Error: {result.get('error', 'Unknown error')}"

    except Exception as e:
        full_answer = f"❌ Sorry, an error occurred: {str(e)}"

    await cl.Message(
        content=full_answer,
        author="Assistant"
    ).send()
