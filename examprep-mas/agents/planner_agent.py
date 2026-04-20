from datetime import datetime

from app.config import MODEL_NAME
from app.state import ExamPrepState
from tools.logging_tools import write_app_log, write_trace_log
from tools.planning_tools import create_study_plan


def planner_agent(state: ExamPrepState) -> ExamPrepState:
    topic = state["topic"]
    time_minutes = state["time_minutes"]
    difficulty = state["difficulty"]

    timestamp = datetime.now().isoformat()

    study_plan = create_study_plan(topic, time_minutes, difficulty)

    log_entry = {
        "timestamp": timestamp,
        "agent": "planner_agent",
        "persona": "Time-constrained study planning assistant",
        "tool_called": "create_study_plan",
        "model_used": MODEL_NAME,
        "input": {
            "topic": topic,
            "time_minutes": time_minutes,
            "difficulty": difficulty
        },
        "output": {
            "study_plan": study_plan,
            "step_count": len(study_plan)
        },
        "status": "success"
    }

    state["study_plan"] = study_plan
    state["logs"].append(log_entry)

    write_app_log(f"Planner Agent executed for topic='{topic}', difficulty='{difficulty}'")
    write_trace_log(log_entry)

    return state