from app.state import ExamPrepState


def content_agent(state: ExamPrepState) -> ExamPrepState:
    study_plan = state["study_plan"]

    # Simple placeholder content
    lesson = f"Lesson generated based on study plan: {', '.join(study_plan)}"

    state["lesson_content"] = lesson

    state["logs"].append({
        "agent": "content_agent",
        "output": lesson
    })

    return state