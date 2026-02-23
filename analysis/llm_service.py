import json
from openai import OpenAI
from analysis.schemas import AnalysisResult
from analysis.prompt_service import SYSTEM_PROMPT, build_user_prompt


client = OpenAI()

# def analyse_resume_and_jd(resume_dict: dict, jd_dict: dict) -> AnalysisResult:
#     user_prompt = build_user_prompt(resume_dict, jd_dict)
#     model = "gpt-4o-mini"
#     temperature = 0

#     response = client.responses.parse(
#         model=model,
#         temperature=temperature,
#         input=[
#             {
#                 "role": "system",
#                 "content": SYSTEM_PROMPT
#             },
#             {
#                 "role": "user",
#                 "content": user_prompt
#             }
#         ],
#         response_format=AnalysisResult
#     )

#     return response.output_parsed

# import json
# from openai import OpenAI
# from app.schemas.analysis_schema import AnalysisResult

# client = OpenAI()


def analyse_resume_and_jd(resume_dict: dict, jd_dict: dict):
    user_prompt = build_user_prompt(resume_dict, jd_dict)
    model = "gpt-4o-mini"
    temperature = 0.2

    response = client.responses.parse(
    model="gpt-4o-2024-08-06",
    temperature=temperature,
    input=[
        {
            "role": "system", 
            "content": SYSTEM_PROMPT},
        {
            "role": "user",
            "content": user_prompt,
        },
    ],
    text_format=AnalysisResult,
    )

    analysis_result = response.output_parsed
    return analysis_result
