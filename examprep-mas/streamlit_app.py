import os
import json
import streamlit as st

from app.graph import build_graph


SUPPORTED_TOPICS = {
    "Machine Learning": "ml.txt",
    "Object-Oriented Programming": "oop.txt",
    "Image Understanding and Processing": "iup.txt",
    "Current Trends in Software Engineering": "ctse.txt",
}


def normalize_topic_to_filename(topic: str) -> str:
    """Convert a topic like 'Machine Learning Basics' to 'machine_learning_basics.txt'."""
    cleaned = topic.strip().lower().replace(" ", "_")
    return f"{cleaned}.txt"


def resolve_notes_file(topic: str, selected_file: str | None = None) -> tuple[str, bool]:
    """
    Resolve the local notes file for the selected or custom topic.

    Args:
        topic: Topic entered or selected by the user.
        selected_file: Explicit pre-mapped notes file for supported topics.

    Returns:
        Tuple of (resolved_file_path, exists_flag).
    """
    if selected_file:
        file_path = os.path.join("data", "notes", selected_file)
        return file_path, os.path.exists(file_path)

    filename = normalize_topic_to_filename(topic)
    file_path = os.path.join("data", "notes", filename)
    return file_path, os.path.exists(file_path)


def initialize_session_state() -> None:
    """Initialize Streamlit session state keys."""
    defaults = {
        "result": None,
        "quiz_generated": False,
        "answers_submitted": False,
        "notes_found": False,
        "notes_path": "",
        "student_answers": [],
        "selected_topic": "",
    }

    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


def build_initial_state(topic: str, time_minutes: int, difficulty: str, notes_file_path: str) -> dict:
    """Build the shared LangGraph state."""
    return {
        "user_request": f"Study {topic} in {time_minutes} minutes",
        "topic": topic,
        "time_minutes": time_minutes,
        "difficulty": difficulty,
        "notes_file_path": notes_file_path,
        "study_plan": [],
        "lesson_content": "",
        "quiz_questions": [],
        "answer_key": [],
        "student_answers": [],
        "evaluation_result": {},
        "logs": []
    }


def save_result(result: dict) -> None:
    """Save final session result to a JSON file."""
    os.makedirs("outputs/session_reports", exist_ok=True)
    with open("outputs/session_reports/result.json", "w", encoding="utf-8") as f:
        json.dump(result, f, indent=4, ensure_ascii=False)


def render_study_plan(plan: list[str]) -> None:
    st.subheader("📘 Study Plan")

    for i, step in enumerate(plan, 1):
        st.markdown(
            f"""
            <div style="
                background-color:#111827;
                padding:14px 16px;
                border-radius:12px;
                margin-bottom:12px;
                border:1px solid #374151;
            ">
                <span style="font-size:18px; font-weight:600; color:#60A5FA;">
                    Step {i}
                </span>
                <div style="margin-top:8px; font-size:16px; line-height:1.6; color:#E5E7EB;">
                    {step}
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )


def render_lesson(content: str) -> None:
    st.subheader("📖 Lesson Content")
    st.markdown(
        f"""
        <div style="
            background-color:#111827;
            padding:16px;
            border-radius:12px;
            border:1px solid #374151;
            line-height:1.7;
            color:#E5E7EB;
        ">
            {content}
        </div>
        """,
        unsafe_allow_html=True
    )


def render_quiz(questions: list) -> list[str]:
    st.subheader("📝 Quiz")
    answers: list[str] = []

    for i, q in enumerate(questions, 1):
        question_text = q if isinstance(q, str) else str(q)
        answer = st.text_input(f"Q{i}: {question_text}", key=f"answer_{i}")
        answers.append(answer)

    return answers


def render_evaluation(result: dict) -> None:
    st.subheader("📊 Evaluation")
    st.write(f"**Score:** {result.get('score')} / {result.get('total')}")
    st.write(f"**Feedback:** {result.get('feedback')}")

    if "weak_areas" in result and result["weak_areas"]:
        st.write("**Weak Areas:**")
        for item in result["weak_areas"]:
            st.write(f"- {item}")

    if "suggestions" in result and result["suggestions"]:
        st.write("**Suggestions:**")
        for item in result["suggestions"]:
            st.write(f"- {item}")


def render_logs(logs: list[dict]) -> None:
    st.subheader("🧾 Logs")
    for log in logs:
        agent_name = log.get("agent", "unknown_agent")
        tool_name = log.get("tool_called")
        if tool_name:
            st.write(f"- {agent_name} executed using `{tool_name}`")
        else:
            st.write(f"- {agent_name} executed")


def main() -> None:
    st.set_page_config(page_title="ExamPrep MAS", page_icon="📚", layout="wide")
    initialize_session_state()

    st.title("📚 ExamPrep MAS")
    st.caption("Multi-Agent Exam Revision System using LangGraph + Ollama")

    with st.form("study_form"):
        topic_mode = st.radio(
            "Topic Selection Mode",
            ["Choose from supported topics", "Enter custom topic"],
            horizontal=True
        )

        selected_file = None

        if topic_mode == "Choose from supported topics":
            selected_topic = st.selectbox("Supported Topics", list(SUPPORTED_TOPICS.keys()))
            topic = selected_topic
            selected_file = SUPPORTED_TOPICS[selected_topic]
        else:
            topic = st.text_input("Custom Topic", placeholder="e.g., Cybersecurity Basics")

        time_minutes = st.number_input(
            "Available Time (minutes)",
            min_value=5,
            max_value=180,
            value=30,
            step=5
        )

        difficulty = st.selectbox("Difficulty", ["easy", "medium", "hard"])

        submitted = st.form_submit_button("Generate Study Session")

    if submitted:
        if not topic.strip():
            st.error("Please enter or select a topic.")
            return

        notes_file_path, notes_found = resolve_notes_file(topic, selected_file)

        st.session_state["notes_found"] = notes_found
        st.session_state["notes_path"] = notes_file_path
        st.session_state["selected_topic"] = topic

        initial_state = build_initial_state(
            topic=topic,
            time_minutes=int(time_minutes),
            difficulty=difficulty,
            notes_file_path=notes_file_path,
        )

        graph = build_graph()
        result = graph.invoke(initial_state)

        st.session_state["result"] = result
        st.session_state["quiz_generated"] = True
        st.session_state["answers_submitted"] = False

    if st.session_state["result"]:
        result = st.session_state["result"]

        if st.session_state["notes_found"]:
            st.success(f"Using local notes file: {st.session_state['notes_path']}")
        else:
            st.warning(
                "No matching local notes file found. "
                "The system should continue in fallback LLM-only mode."
            )

        render_study_plan(result["study_plan"])
        render_lesson(result["lesson_content"])
        answers = render_quiz(result["quiz_questions"])

        if st.button("Evaluate Answers"):
            result["student_answers"] = answers

            graph = build_graph()
            updated_result = graph.invoke(result)

            st.session_state["result"] = updated_result
            st.session_state["answers_submitted"] = True
            save_result(updated_result)

    if st.session_state["result"] and st.session_state["answers_submitted"]:
        result = st.session_state["result"]
        render_evaluation(result["evaluation_result"])
        render_logs(result["logs"])


if __name__ == "__main__":
    main()