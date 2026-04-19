from app.state import ExamPrepState


def evaluator_agent(state: ExamPrepState) -> ExamPrepState:
    # Dummy evaluation (no real user answers yet)
    result = {
        "score": 0,
        "total": len(state["quiz_questions"]),
        "feedback": "Evaluation placeholder"
    }

    state["evaluation_result"] = result

    state["logs"].append({
        "agent": "evaluator_agent",
        "output": result
    })

    return state