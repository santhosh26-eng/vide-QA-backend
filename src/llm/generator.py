import os

from dotenv import load_dotenv
from mistralai import Mistral

from src.prompts.system_prompt import SYSTEM_PROMPT
from src.utils.logger import logger
from src.utils.retry import retry

from src.database.chat_db import save_chat

load_dotenv()

client = Mistral(
    api_key=os.getenv("MISTRAL_API_KEY")
)


def generate_answer(question, chunks):
    """
    Normal response (used by test_llm.py)
    """

    context = "\n\n".join(chunks)

    response = retry(
        lambda: client.chat.complete(
            model="mistral-small-latest",
            messages=[
                {
                    "role": "system",
                    "content": SYSTEM_PROMPT
                },
                {
                    "role": "user",
                    "content": f"""
Context:
{context}

Question:
{question}
"""
                }
            ]
        )
    )

    return response.choices[0].message.content


async def stream_answer(video_id, question, chunks):
    """
    Streaming response for FastAPI.
    Saves the completed chat into MongoDB after streaming.
    """

    logger.info("Streaming started...")

    context = "\n\n".join(chunks)

    stream = client.chat.stream(
        model="mistral-small-latest",
        messages=[
            {
                "role": "system",
                "content": SYSTEM_PROMPT
            },
            {
                "role": "user",
                "content": f"""
Context:
{context}

Question:
{question}
"""
            }
        ]
    )

    # Store complete answer
    complete_answer = ""

    for event in stream:

        if event.data.choices:

            delta = event.data.choices[0].delta.content

            if delta:
                complete_answer += delta
                yield delta

    # Save chat history to MongoDB
    try:
        await save_chat(
            video_id=video_id,
            question=question,
            answer=complete_answer
        )
        logger.info("Chat saved successfully to MongoDB.")
    except Exception as e:
        logger.error(f"Failed to save chat to MongoDB: {e}")

    logger.info("Streaming finished.")