from app.state import ExamPrepState
from tools.planning_tools import create_study_plan


def planner_agent(state: ExamPrepState) -> ExamPrepState:
    topic = state["topic"]
    time_minutes = state["time_minutes"]
    difficulty = state["difficulty"]

    study_plan = create_study_plan(topic, time_minutes, difficulty)

    state["study_plan"] = study_plan
    state["logs"].append({
        "agent": "planner_agent",
        "input": {
            "topic": topic,
            "time_minutes": time_minutes,
            "difficulty": difficulty
        },
        "output": {
            "study_plan": study_plan
        }
    })

    return state