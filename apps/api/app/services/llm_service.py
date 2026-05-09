import os
from groq import Groq

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)


def generate_streaming_answer(query: str, context: str):

    prompt = f"""
You are Resolvr AI.

Answer ONLY from the provided context.

If the answer is not in the context, say:
"I could not find this information in the uploaded documents."

Context:
{context}

Question:
{query}
"""

    stream = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.2,
        stream=True
    )

    for chunk in stream:

        content = chunk.choices[0].delta.content

        if content:
            yield content