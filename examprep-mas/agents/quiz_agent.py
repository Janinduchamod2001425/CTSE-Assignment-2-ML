from app.state import ExamPrepState


def quiz_agent(state: ExamPrepState) -> ExamPrepState:
    content = state["lesson_content"]

    # Simple placeholder quiz
    questions = [
        "What is the main topic discussed?",
        "Mention one key concept."
    ]

    answers = [
        "Machine Learning",
        "Supervised Learning"
    ]

    state["quiz_questions"] = questions
    state["answer_key"] = answers

    state["logs"].append({
        "agent": "quiz_agent",
        "output": questions
    })

    return state