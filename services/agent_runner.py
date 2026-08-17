import asyncio
import json
import os
import uuid

from dotenv import load_dotenv

load_dotenv()

from google.genai import types

from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService

from agents.resume_parser_agent.agent import (
    root_agent as resume_parser_agent
)

from agents.ats_evaluator_agent.agent import (
    root_agent as ats_evaluator_agent
)

APP_NAME = "resume_manager"

session_service = InMemorySessionService()

# --------------------------------------------------
# Resume Parser Runner
# --------------------------------------------------

resume_runner = Runner(
    app_name=APP_NAME,
    agent=resume_parser_agent,
    session_service=session_service
)

# --------------------------------------------------
# ATS Evaluator Runner
# --------------------------------------------------

ats_runner = Runner(
    app_name=APP_NAME,
    agent=ats_evaluator_agent,
    session_service=session_service
)


async def run_resume_parser(prompt):

    session = await session_service.create_session(
        app_name=APP_NAME,
        user_id="streamlit_user",
        session_id=f"resume_session_{uuid.uuid4()}"
    )

    user_message = types.Content(
        role="user",
        parts=[
            types.Part(text=prompt)
        ]
    )

    final_response = ""

    async for event in resume_runner.run_async(
        user_id="streamlit_user",
        session_id=session.id,
        new_message=user_message
    ):

        if (
            hasattr(event, "content")
            and event.content
            and hasattr(event.content, "parts")
        ):
            for part in event.content.parts:

                if hasattr(part, "text"):

                    final_response += part.text

    try:
        return json.loads(final_response)

    except Exception:
        return {
            "name": "",
            "email": "",
            "phone": "",
            "skills": [],
            "education": [],
            "experience": [],
            "projects": [],
            "certifications": []
    }

def run_resume_parser_sync(prompt):

    return asyncio.run(
        run_resume_parser(prompt)
    )


# --------------------------------------------------
# ATS Evaluator
# --------------------------------------------------

async def run_ats_evaluator(
    candidate_profile,
    job_description
):

    session = await session_service.create_session(
        app_name=APP_NAME,
        user_id="streamlit_user",
        session_id=f"ats_session_{uuid.uuid4()}"
    )

    prompt = f"""
Candidate Profile:

{json.dumps(candidate_profile, indent=2)}

Job Description:

{json.dumps(job_description, indent=2)}

Evaluate this candidate.

Return ONLY JSON.
"""

    user_message = types.Content(
        role="user",
        parts=[
            types.Part(text=prompt)
        ]
    )

    final_response = ""

    async for event in ats_runner.run_async(
        user_id="streamlit_user",
        session_id=session.id,
        new_message=user_message
    ):

        if (
            hasattr(event, "content")
            and event.content
            and hasattr(event.content, "parts")
        ):
            for part in event.content.parts:

                if hasattr(part, "text"):

                    final_response += part.text

    try:
        return json.loads(final_response)

    except Exception:
        return {
            "ats_score": 0,
            "recommendation": "Unable to Evaluate",
            "strengths": [],
            "gaps": [],
            "summary": final_response
        }


def run_ats_evaluator_sync(
    candidate_profile,
    job_description
):

    return asyncio.run(
        run_ats_evaluator(
            candidate_profile,
            job_description
        )
    )