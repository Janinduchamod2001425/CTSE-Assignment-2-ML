from typing import List

from langchain_ollama import ChatOllama

from app.config import MODEL_NAME, MAX_PLAN_STEPS, OLLAMA_TEMPERATURE
from prompts.planner_prompt import PLANNER_PROMPT_TEMPLATE


llm = ChatOllama(
    model=MODEL_NAME,
    temperature=OLLAMA_TEMPERATURE,
)


def _clean_plan_lines(raw_text: str) -> List[str]:
    """
    Clean model output into a list of study plan steps.

    Args:
        raw_text: Raw text returned by the language model.

    Returns:
        A cleaned list of non-empty study steps.
    """
    lines = raw_text.strip().splitlines()
    cleaned_steps: List[str] = []

    for line in lines:
        step = line.strip()

        if not step:
            continue

        # Remove common numbering formats like "1. ", "2) ", "- "
        if len(step) > 2 and step[0].isdigit():
            if ". " in step[:4]:
                step = step.split(". ", 1)[1]
            elif ") " in step[:4]:
                step = step.split(") ", 1)[1]

        if step.startswith("- "):
            step = step[2:].strip()

        if step:
            cleaned_steps.append(step)

    return cleaned_steps


def create_study_plan(topic: str, minutes: int, difficulty: str) -> List[str]:
    """
    Generate a structured study plan using a local Ollama model.

    Args:
        topic: Study topic provided by the user.
        minutes: Available study time in minutes.
        difficulty: Requested difficulty level.

    Returns:
        A list of ordered study steps.

    Raises:
        ValueError: If topic is empty or minutes is less than or equal to zero.
    """
    topic = topic.strip()
    difficulty = difficulty.strip().lower()

    if not topic:
        raise ValueError("topic must not be empty")

    if minutes <= 0:
        raise ValueError("minutes must be greater than 0")

    if difficulty not in {"easy", "medium", "hard"}:
        raise ValueError("difficulty must be one of: easy, medium, hard")

    prompt = PLANNER_PROMPT_TEMPLATE.format(
        topic=topic,
        minutes=minutes,
        difficulty=difficulty,
        max_steps=MAX_PLAN_STEPS,
    )

    response = llm.invoke(prompt)
    raw_output = response.content if hasattr(response, "content") else str(response)

    steps = _clean_plan_lines(raw_output)

    if not steps:
        raise ValueError("model returned an empty study plan")

    return steps[:MAX_PLAN_STEPS]