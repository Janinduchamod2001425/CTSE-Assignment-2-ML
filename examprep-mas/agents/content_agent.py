# from typing import Any, Dict

# import ollama

# from prompts.content_prompt import CONTENT_PROMPT
# from tools.notes_tools import read_notes


# def content_agent(state: Dict[str, Any]) -> Dict[str, Any]:
#     """
#     Generate lesson content using local notes, study plan, and user preferences.

#     Args:
#         state: Shared LangGraph state.

#     Returns:
#         Updated state with lesson_content and logs.
#     """
#     topic = state.get("topic", "").strip()
#     time_minutes = state.get("time_minutes", 0)
#     difficulty = state.get("difficulty", "medium")
#     study_plan = state.get("study_plan", [])
#     logs = state.setdefault("logs", [])

#     try:
#         notes = read_notes(topic)

#         user_prompt = f"""
# Topic: {topic}
# Time available: {time_minutes} minutes
# Difficulty: {difficulty}

# Study plan:
# {chr(10).join(f"- {item}" for item in study_plan)}

# Lecture notes:
# {notes}
# """

#         response = ollama.chat(
#             model="qwen2.5:3b",
#             messages=[
#                 {"role": "system", "content": CONTENT_PROMPT},
#                 {"role": "user", "content": user_prompt},
#             ],
#         )

#         lesson_content = response["message"]["content"].strip()

#         state["lesson_content"] = lesson_content

#         logs.append(
#             {
#                 "agent": "content_agent",
#                 "status": "success",
#                 "topic": topic,
#                 "study_plan_count": len(study_plan),
#                 "output_preview": lesson_content[:200],
#             }
#         )

#     except Exception as e:
#         state["lesson_content"] = ""
#         logs.append(
#             {
#                 "agent": "content_agent",
#                 "status": "error",
#                 "topic": topic,
#                 "error": str(e),
#             }
#         )

#     return state

#new one
from typing import Any, Dict
import os
import json
import ollama

from prompts.content_prompt import CONTENT_PROMPT
from tools.notes_tools import read_notes


# =========================
# Helper Functions
# =========================

def _ensure_structure(text: str, study_plan: list) -> str:
    """Ensure output follows required structure."""
    if "# Topic:" in text and "Final Quick Revision Summary" in text:
        return text

    sections = "\n".join(
        f"## {i+1}. {s}\n- (content missing)" for i, s in enumerate(study_plan)
    )

    return f"# Topic: Generated\n\n{sections}\n\n## Final Quick Revision Summary\n- Key points"


def _uses_notes_only(output: str, notes: str) -> bool:
    """Basic check to ensure output relates to notes."""
    note_words = notes.split()[:50]
    return any(word.lower() in output.lower() for word in note_words)


# =========================
# Main Agent
# =========================

def content_agent(state: Dict[str, Any]) -> Dict[str, Any]:

    # =========================
    # 1. State Validation
    # =========================
    required_keys = ["topic", "time_minutes", "difficulty", "study_plan"]
    for key in required_keys:
        if key not in state:
            raise KeyError(f"Missing required state key: {key}")

    topic = state.get("topic", "").strip()
    time_minutes = state.get("time_minutes", 0)
    difficulty = state.get("difficulty", "medium").lower()
    study_plan = state.get("study_plan", [])
    logs = state.setdefault("logs", [])

    #  helper to write trace file
    def write_trace(entry):
        os.makedirs("logs", exist_ok=True)
        with open("logs/execution_trace.jsonl", "a", encoding="utf-8") as f:
            f.write(json.dumps(entry) + "\n")

    try:
        # =========================
        #  2. INPUT LOGGING
        # =========================
        input_log = {
            "stage": "input_received",
            "agent": "content_agent",
            "input": {
                "topic": topic,
                "difficulty": difficulty,
                "time_minutes": time_minutes,
                "study_plan": study_plan,
            },
        }
        logs.append(input_log)
        write_trace(input_log)

        # =========================
        #  3. TOOL CALL LOGGING
        # =========================
        tool_call_log = {
            "stage": "tool_call",
            "tool": "read_notes",
            "input": topic,
        }
        logs.append(tool_call_log)
        write_trace(tool_call_log)

        try:
            notes = read_notes(topic)
        except Exception:
            notes = "Basic notes not available. Provide simple explanation."

        tool_output_log = {
            "stage": "tool_output",
            "tool": "read_notes",
            "output_preview": notes[:100],
        }
        logs.append(tool_output_log)
        write_trace(tool_output_log)

        # =========================
        # 4. Difficulty Guidance
        # =========================
        if difficulty == "easy":
            difficulty_guidance = "Explain in very simple terms using short sentences."
        elif difficulty == "hard":
            difficulty_guidance = "Provide deeper technical explanations."
        else:
            difficulty_guidance = "Provide balanced explanations."

        # =========================
        # 5. Time Guidance
        # =========================
        if time_minutes <= 15:
            time_guidance = "Keep explanations very short."
        elif time_minutes <= 30:
            time_guidance = "Provide moderate detail."
        else:
            time_guidance = "Provide detailed explanations."

        # =========================
        # 6. Prompt Build
        # =========================
        user_prompt = f"""
Topic: {topic}
Difficulty: {difficulty}
Time available: {time_minutes} minutes

Guidance:
{difficulty_guidance}

Time Guidance:
{time_guidance}

Study Plan:
{chr(10).join(f"- {item}" for item in study_plan)}

Lecture Notes:
{notes}
"""

        # =========================
        #  7. LLM CALL LOGGING
        # =========================
        llm_call_log = {
            "stage": "llm_call",
            "model": "qwen2.5:3b",
            "prompt_preview": user_prompt[:200],
        }
        logs.append(llm_call_log)
        write_trace(llm_call_log)

        response = ollama.chat(
            model="qwen2.5:3b",
            messages=[
                {"role": "system", "content": CONTENT_PROMPT},
                {"role": "user", "content": user_prompt},
            ],
        )

        lesson_content = response["message"]["content"].strip()

        # =========================
        # 8. Structure + Validation
        # =========================
        lesson_content = _ensure_structure(lesson_content, study_plan)

        if not _uses_notes_only(lesson_content, notes):
            lesson_content = "# Topic: " + topic + "\n\nContent could not be verified."

        # =========================
        # 9. Update State
        # =========================
        state["lesson_content"] = lesson_content

        # =========================
        #  10. OUTPUT LOGGING
        # =========================
        output_log = {
            "stage": "output_generated",
            "agent": "content_agent",
            "status": "success",
            "output_length": len(lesson_content),
            "output_preview": lesson_content[:200],
        }
        logs.append(output_log)
        write_trace(output_log)

    except Exception as e:
        state["lesson_content"] = ""

        error_log = {
            "stage": "error",
            "agent": "content_agent",
            "error": str(e),
        }
        logs.append(error_log)
        write_trace(error_log)

    return state