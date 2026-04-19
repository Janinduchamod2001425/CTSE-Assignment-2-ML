from typing import Any, Dict

import ollama

from prompts.content_prompt import CONTENT_PROMPT
from tools.notes_tools import read_notes


def content_agent(state: Dict[str, Any]) -> Dict[str, Any]:
    """
    Generate lesson content using local notes, study plan, and user preferences.

    Args:
        state: Shared LangGraph state.

    Returns:
        Updated state with lesson_content and logs.
    """
    topic = state.get("topic", "").strip()
    time_minutes = state.get("time_minutes", 0)
    difficulty = state.get("difficulty", "medium")
    study_plan = state.get("study_plan", [])
    logs = state.setdefault("logs", [])

    try:
        notes = read_notes(topic)

        user_prompt = f"""
Topic: {topic}
Time available: {time_minutes} minutes
Difficulty: {difficulty}

Study plan:
{chr(10).join(f"- {item}" for item in study_plan)}

Lecture notes:
{notes}
"""

        response = ollama.chat(
            model="qwen2.5:3b",
            messages=[
                {"role": "system", "content": CONTENT_PROMPT},
                {"role": "user", "content": user_prompt},
            ],
        )

        lesson_content = response["message"]["content"].strip()

        state["lesson_content"] = lesson_content

        logs.append(
            {
                "agent": "content_agent",
                "status": "success",
                "topic": topic,
                "study_plan_count": len(study_plan),
                "output_preview": lesson_content[:200],
            }
        )

    except Exception as e:
        state["lesson_content"] = ""
        logs.append(
            {
                "agent": "content_agent",
                "status": "error",
                "topic": topic,
                "error": str(e),
            }
        )

    return state