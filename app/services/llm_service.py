from openai import OpenAI
import os

client=  OpenAI(
    api_key =os.getenv("OPENROUTER_API_KEY"),
    base_url="https://openrouter.ai/api/v1"
)

def generate_answer(question,context):
    prompt = f"""
You are a pet insurance assistant.

Answer ONLY using the policy context.

Policy Context:
{context}

Question:
{question}
"""
    
    response= client.chat.completions.create(
        model="deepseek/deepseek-chat-v3-0324",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )
    return response.choices[0].message.content