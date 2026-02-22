import json
from services.llm_client import LLMClient
from job_descriptions.prompt_service import SYSTEM_PROMPT, build_user_prompt

def parse_job_description_with_llm(text: str) -> dict:
    llm = LLMClient(model="gpt-4o-mini")

    response = llm.chat(
        system_prompt=SYSTEM_PROMPT,
        user_prompt=build_user_prompt(text),
        temperature=0.0,
    )

    try:
        return json.loads(response)
    except json.JSONDecodeError:
        raise ValueError("LLM returned invalid JSON")