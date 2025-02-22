import chainlit as cl
import requests
from typing import Dict, Any
import logging
import os
import httpx

@cl.on_chat_start
async def start():
    """Initialize the chat session."""
    api_url = os.getenv("BACKEND_URL", "http://localhost:8000")
    cl.user_session.set("api_url", api_url)

    await cl.Message(
        content="👋 Hello! I'm your company knowledge assistant. You can upload PDF documents and ask questions about them.",
        author="Assistant"
    ).send()

@cl.on_message
async def main(message: cl.Message):
    """Handle incoming messages."""
    api_url = cl.user_session.get("api_url")

    try:
        response = requests.post(
            f"{api_url}/ask",
            json={"text": message.content}
        )
        response.raise_for_status()
        result = response.json()

        if result["status"] == "success":
            await cl.Message(
                content=result["answer"],
                author="Assistant"
            ).send()
        else:
            await cl.Message(
                content=f"Error: {result.get('error', 'Unknown error')}",
                author="Assistant"
            ).send()

    except Exception as e:
        await cl.Message(
            content=f"Sorry, an error occurred: {str(e)}",
            author="Assistant"
        ).send()

@cl.on_message
async def handle_file(message: cl.Message):
    if message.files:
        api_url = cl.user_session.get("api_url")

        async with httpx.AsyncClient() as client:
            for file in message.files:
                try:
                    await cl.Message(
                        content=f"Uploading file '{file.name}'...",
                        author="Assistant"
                    ).send()

                    files = {'file': (file.name, file.content)}
                    response = await client.post(f"{api_url}/upload", files=files)
                    response.raise_for_status()

                    await cl.Message(
                        content=f"✅ File '{file.name}' uploaded successfully! You can now ask questions about its contents.",
                        author="Assistant"
                    ).send()

                except httpx.HTTPStatusError as e:
                    await cl.Message(
                        content=f"❌ Error uploading file '{file.name}': HTTP {e.response.status_code} - {e.response.text}",
                        author="Assistant"
                    ).send()
                except Exception as e:
                    await cl.Message(
                        content=f"❌ Error uploading file '{file.name}': {str(e)}",
                        author="Assistant"
                    ).send()
