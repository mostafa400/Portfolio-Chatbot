from openai import OpenAI
from config import OPENROUTER_API_KEY, SYSTEM_PROMPT

client = OpenAI(
    api_key=OPENROUTER_API_KEY,
    base_url="https://openrouter.ai/api/v1"
)


async def get_chat_response(messages: list) -> str:
    """Get response from OpenRouter"""
    try:
        completion = client.chat.completions.create(
            model="anthropic/claude-3.5-haiku",  # or "openai/gpt-3.5-turbo"
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                *messages
            ],
            max_tokens=500,
            temperature=0.7,
        )
        return completion.choices[0].message.content
    except Exception as e:
        print(f"OpenRouter Error: {e}")
        raise
