import os
from groq import Groq

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)


def generate_answer(query: str, context: str):

    # --- LIMIT CONTEXT SIZE ---
    context = context[:4000]

    prompt = f"""
You are Resolvr AI, an intelligent enterprise document assistant.

Your job:
- Answer ONLY using the provided context
- Give concise and professional answers
- Do NOT hallucinate
- If answer is missing, say:
"I could not find this information in the uploaded documents."

Context:
{context}

User Question:
{query}

Answer:
"""

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {
                "role": "system",
                "content": "You are a precise RAG assistant."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.1,
        max_tokens=300
    )

    return response.choices[0].message.content