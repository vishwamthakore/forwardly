import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")


class LLMClient:
    def __init__(self, model: str = "gpt-4o-mini"):
        self.client = OpenAI(api_key=OPENAI_API_KEY)
        self.model = model

    def chat(self, system_prompt: str, user_prompt: str, temperature: float = 0.0):
        response = self.client.chat.completions.create(
            model=self.model,
            temperature=temperature,
            response_format={"type": "json_object"},
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
        )

        return response.choices[0].message.content
