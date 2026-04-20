from typing import List
from langchain_ollama import ChatOllama

from app.config import MODEL_NAME, MAX_PLAN_STEPS, OLLAMA_TEMPERATURE
from prompts.planner_prompt import PLANNER_PROMPT_TEMPLATE


llm = ChatOllama(
    model=MODEL_NAME,
    temperature=OLLAMA_TEMPERATURE,
)


def _clean_plan_lines(raw_text: str) -> List[str]:
    lines = raw_text.strip().splitlines()
    cleaned_steps: List[str] = []

    for line in lines:
        step = line.strip()

        if not step:
            continue

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


def _fallback_plan(topic: str, difficulty: str) -> List[str]:
    base_plan = [
        f"Review the definition and purpose of {topic}.",
        f"Study the main concepts and principles of {topic}.",
        f"Examine key examples or practical applications of {topic}.",
        f"Practice a few concept-based questions related to {topic}.",
        f"Summarize the most important points of {topic} for quick revision."
    ]

    if difficulty == "hard":
        base_plan.insert(3, f"Analyze more advanced or challenging aspects of {topic}.")

    return base_plan[:MAX_PLAN_STEPS]


def create_study_plan(topic: str, minutes: int, difficulty: str) -> List[str]:
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

    try:
        response = llm.invoke(prompt)
        raw_output = response.content if hasattr(response, "content") else str(response)
        steps = _clean_plan_lines(raw_output)

        # fallback if too weak
        if not steps or len(steps) < 3:
            steps = _fallback_plan(topic, difficulty)

    except Exception:
        steps = _fallback_plan(topic, difficulty)

    return steps[:MAX_PLAN_STEPS]