from langgraph.graph import StateGraph, END

from app.state import ExamPrepState
from agents.planner_agent import planner_agent
from agents.content_agent import content_agent
from agents.quiz_agent import quiz_agent
from agents.evaluator_agent import evaluator_agent


def build_graph():
    print("Building LangGraph workflow...")

    builder = StateGraph(ExamPrepState)

    builder.add_node("planner", planner_agent)
    builder.add_node("content", content_agent)
    builder.add_node("quiz", quiz_agent)
    builder.add_node("evaluator", evaluator_agent)

    builder.set_entry_point("planner")

    builder.add_edge("planner", "content")
    builder.add_edge("content", "quiz")
    builder.add_edge("quiz", "evaluator")
    builder.add_edge("evaluator", END)

    return builder.compile()