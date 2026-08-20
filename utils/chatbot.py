import os
import time

from dotenv import load_dotenv
from google import genai


# Load environment variables
load_dotenv()

# Create Gemini client
client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)


def generate_answer(question, context):
    """
    Generate an answer using Gemini based only on
    the retrieved PDF context.
    """

    prompt = f"""
You are an AI assistant that answers questions about an uploaded PDF.

IMPORTANT RULES:
1. Answer ONLY using the information provided in the context.
2. Do not use outside knowledge.
3. If the answer is not present in the context, say:
   "I couldn't find the answer in the uploaded PDF."
4. Give a clear and concise answer.
5. Do not invent facts.

CONTEXT FROM PDF:
{context}

USER QUESTION:
{question}

ANSWER:
"""

    # Retry if Gemini is temporarily unavailable
    for attempt in range(3):

        try:

            response = client.models.generate_content(
                model="gemini-3.7-flash",
                contents=prompt
            )

            return response.text

        except Exception as e:

            if attempt < 2:
                print(
                    f"Gemini temporarily unavailable. "
                    f"Retrying... ({attempt + 1}/3)"
                )

                time.sleep(3)

            else:
                raise e