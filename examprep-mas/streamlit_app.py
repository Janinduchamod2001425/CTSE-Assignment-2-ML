import os
import json
import streamlit as st
from datetime import datetime

from app.graph import build_full_graph

SUPPORTED_TOPICS = {
    "Machine Learning": "ml.txt",
    "Object-Oriented Programming": "oop.txt",
    "Image Understanding and Processing": "iup.txt",
    "Current Trends in Software Engineering": "ctse.txt",
}


# Custom CSS for professional styling
def apply_custom_css():
    st.markdown("""
        <style>
        /* Main container styling */
        .main {
            background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        }

        /* Card styling */
        .custom-card {
            background: white;
            border-radius: 16px;
            padding: 24px;
            margin-bottom: 20px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.07), 0 1px 3px rgba(0, 0, 0, 0.05);
            transition: transform 0.2s ease, box-shadow 0.2s ease;
        }

        .custom-card:hover {
            transform: translateY(-2px);
            box-shadow: 0 10px 25px rgba(0, 0, 0, 0.1);
        }

        /* Header styling */
        .main-header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 2rem;
            border-radius: 20px;
            margin-bottom: 2rem;
            text-align: center;
            color: white;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
        }

        .main-header h1 {
            margin: 0;
            font-size: 2.5rem;
            font-weight: 700;
        }

        .main-header p {
            margin: 0.5rem 0 0 0;
            opacity: 0.95;
            font-size: 1.1rem;
        }

        /* Study plan step styling */
        .study-step {
            background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
            padding: 16px;
            border-radius: 12px;
            margin-bottom: 12px;
            border-left: 4px solid #667eea;
            transition: all 0.3s ease;
        }

        .study-step:hover {
            transform: translateX(5px);
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
        }

        .step-number {
            font-weight: 700;
            color: #667eea;
            font-size: 1.1rem;
            margin-bottom: 8px;
        }

        .step-content {
            color: #2c3e50;
            line-height: 1.6;
        }

        /* Lesson content styling */
        .lesson-content {
            background: #f8f9fa;
            padding: 24px;
            border-radius: 12px;
            border: 1px solid #dee2e6;
            line-height: 1.8;
            color: #2c3e50;
            font-size: 1rem;
        }

        /* Quiz styling */
        .quiz-question {
            background: #ffffff;
            padding: 20px;
            border-radius: 12px;
            margin-bottom: 20px;
            border: 2px solid #e9ecef;
            transition: all 0.3s ease;
        }

        .quiz-question:hover {
            border-color: #667eea;
            box-shadow: 0 4px 12px rgba(102, 126, 234, 0.1);
        }

        .question-text {
            font-weight: 600;
            color: #2c3e50;
            margin-bottom: 12px;
            font-size: 1.05rem;
        }

        /* Score display */
        .score-card {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 24px;
            border-radius: 16px;
            text-align: center;
            color: white;
            margin-bottom: 20px;
        }

        .score-number {
            font-size: 3rem;
            font-weight: 700;
            margin: 10px 0;
        }

        .feedback-text {
            background: #d4edda;
            color: #155724;
            padding: 16px;
            border-radius: 10px;
            border-left: 4px solid #28a745;
            margin: 16px 0;
        }

        /* Badge styling */
        .badge {
            display: inline-block;
            padding: 4px 12px;
            border-radius: 20px;
            font-size: 0.85rem;
            font-weight: 600;
            margin-right: 8px;
        }

        .badge-easy {
            background: #28a745;
            color: white;
        }

        .badge-medium {
            background: #ffc107;
            color: #856404;
        }

        .badge-hard {
            background: #dc3545;
            color: white;
        }

        /* Button styling */
        .stButton > button {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            padding: 0.65rem 1.5rem;
            font-weight: 600;
            border-radius: 10px;
            transition: all 0.3s ease;
            width: 100%;
        }

        .stButton > button:hover {
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
        }

        /* Sidebar styling */
        .css-1d391kg {
            background: linear-gradient(180deg, #2c3e50 0%, #34495e 100%);
        }

        /* Progress indicator */
        .progress-step {
            display: inline-block;
            width: 30px;
            height: 30px;
            border-radius: 50%;
            background: #e9ecef;
            text-align: center;
            line-height: 30px;
            margin: 0 5px;
            font-weight: 600;
        }

        .progress-step.active {
            background: #667eea;
            color: white;
        }

        .progress-step.completed {
            background: #28a745;
            color: white;
        }

        /* Info box */
        .info-box {
            background: #e7f3ff;
            border-left: 4px solid #2196f3;
            padding: 16px;
            border-radius: 8px;
            margin: 16px 0;
        }

        /* Timer styling */
        .timer-box {
            background: #2c3e50;
            color: white;
            padding: 12px;
            border-radius: 10px;
            text-align: center;
            font-size: 1.2rem;
            font-weight: 600;
        }
        </style>
    """, unsafe_allow_html=True)


def normalize_topic_to_filename(topic: str) -> str:
    cleaned = topic.strip().lower().replace(" ", "_")
    return f"{cleaned}.txt"


def resolve_notes_file(topic: str, selected_file: str | None = None) -> tuple[str, bool]:
    if selected_file:
        file_path = os.path.join("data", "notes", selected_file)
        return file_path, os.path.exists(file_path)
    filename = normalize_topic_to_filename(topic)
    file_path = os.path.join("data", "notes", filename)
    return file_path, os.path.exists(file_path)


def initialize_session_state() -> None:
    defaults = {
        "result": None,
        "quiz_generated": False,
        "answers_submitted": False,
        "notes_found": False,
        "notes_path": "",
        "student_answers": [],
        "selected_topic": "",
        "session_start_time": None,
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


def build_initial_state(topic: str, time_minutes: int, difficulty: str, notes_file_path: str) -> dict:
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
    os.makedirs("outputs/session_reports", exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"outputs/session_reports/result_{timestamp}.json"
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=4, ensure_ascii=False)


def render_sidebar_info(topic: str, difficulty: str, time_minutes: int, notes_found: bool):
    with st.sidebar:
        st.markdown("### 🎯 Session Info")

        if topic:
            st.markdown(f"**Topic:** {topic}")

        difficulty_colors = {"easy": "🟢 Easy", "medium": "🟡 Medium", "hard": "🔴 Hard"}
        if difficulty in difficulty_colors:
            st.markdown(f"**Difficulty:** {difficulty_colors[difficulty]}")

        if time_minutes:
            st.markdown(f"**Time:** ⏱️ {time_minutes} minutes")

        if notes_found:
            st.success("📄 Local notes available")
        else:
            st.info("🌐 Using LLM knowledge base")

        st.markdown("---")
        st.markdown("### 🤖 Agents Working")
        st.markdown("""
        - 📋 **Planner Agent** - Creates study structure
        - 📚 **Content Agent** - Generates lessons
        - ✍️ **Quiz Agent** - Creates assessments
        - 📊 **Evaluator Agent** - Grades & provides feedback
        """)

        st.markdown("---")
        st.markdown("### 💡 Pro Tips")
        st.markdown("""
        - Be specific with your topic
        - Choose appropriate difficulty
        - Review weak areas after quiz
        """)


def render_study_plan(plan: list[str]) -> None:
    st.markdown('<div class="custom-card">', unsafe_allow_html=True)
    st.markdown("### 📋 Study Plan")
    st.markdown("*Your personalized learning journey*")

    for i, step in enumerate(plan, 1):
        st.markdown(f"""
        <div class="study-step">
            <div class="step-number">Step {i}</div>
            <div class="step-content">{step}</div>
        </div>
        """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)


def render_lesson(content: str) -> None:
    st.markdown('<div class="custom-card">', unsafe_allow_html=True)
    st.markdown("### 📖 Learning Material")

    if len(content) > 500:
        with st.expander("📚 View Full Lesson Content", expanded=True):
            st.markdown(f'<div class="lesson-content">{content}</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="lesson-content">{content}</div>', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)


def render_quiz(questions: list) -> list[str]:
    st.markdown('<div class="custom-card">', unsafe_allow_html=True)
    st.markdown("### ✍️ Knowledge Check")
    st.markdown("*Answer these questions to test your understanding*")

    answers: list[str] = []

    for i, q in enumerate(questions, 1):
        question_text = q if isinstance(q, str) else str(q)
        st.markdown(f"""
        <div class="quiz-question">
            <div class="question-text">Question {i}</div>
            <div>{question_text}</div>
        </div>
        """, unsafe_allow_html=True)
        answer = st.text_area(f"Your Answer", key=f"answer_{i}",
                              placeholder="Type your answer here...", height=100)
        answers.append(answer)

    st.markdown('</div>', unsafe_allow_html=True)
    return answers


def render_evaluation(result: dict) -> None:
    st.markdown('<div class="custom-card">', unsafe_allow_html=True)
    st.markdown("### 📊 Performance Analysis")

    score = result.get('score', 0)
    total = result.get('total', 1)
    percentage = (score / total) * 100 if total > 0 else 0

    # Score display
    st.markdown(f"""
    <div class="score-card">
        <div>Your Score</div>
        <div class="score-number">{score} / {total}</div>
        <div style="font-size: 1.2rem;">{percentage:.1f}%</div>
    </div>
    """, unsafe_allow_html=True)

    # Feedback
    feedback = result.get('feedback', '')
    if feedback:
        st.markdown(f'<div class="feedback-text">💬 {feedback}</div>', unsafe_allow_html=True)

    # Weak areas
    if "weak_areas" in result and result["weak_areas"]:
        st.markdown("#### 🎯 Areas for Improvement")
        for item in result["weak_areas"]:
            st.markdown(f"- ⚠️ {item}")

    # Suggestions
    if "suggestions" in result and result["suggestions"]:
        st.markdown("#### 💡 Recommendations")
        for item in result["suggestions"]:
            st.markdown(f"- ✅ {item}")

    st.markdown('</div>', unsafe_allow_html=True)


def render_logs(logs: list[dict]) -> None:
    with st.expander("🔍 View System Logs", expanded=False):
        for log in logs:
            agent_name = log.get("agent", "unknown_agent")
            tool_name = log.get("tool_called")
            if tool_name:
                st.markdown(f"- **{agent_name}** → used `{tool_name}`")
            else:
                st.markdown(f"- **{agent_name}** executed")


def render_progress_bar(current_step: str):
    steps = ["Plan", "Learn", "Quiz", "Evaluate"]
    current_index = steps.index(current_step) if current_step in steps else 0

    cols = st.columns(len(steps))
    for idx, (col, step) in enumerate(zip(cols, steps)):
        with col:
            if idx < current_index:
                st.markdown(
                    f'<div style="text-align:center"><span class="progress-step completed">✓</span><br>{step}</div>',
                    unsafe_allow_html=True)
            elif idx == current_index:
                st.markdown(
                    f'<div style="text-align:center"><span class="progress-step active">{idx + 1}</span><br>{step}</div>',
                    unsafe_allow_html=True)
            else:
                st.markdown(
                    f'<div style="text-align:center"><span class="progress-step">{idx + 1}</span><br>{step}</div>',
                    unsafe_allow_html=True)


def main() -> None:
    st.set_page_config(
        page_title="ExamPrep MAS - Intelligent Study Assistant",
        page_icon="🎓",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    apply_custom_css()
    initialize_session_state()

    # Header
    st.markdown("""
    <div class="main-header">
        <h1>🎓 ExamPrep MAS</h1>
        <p>Multi-Agent System for Intelligent Exam Preparation</p>
        <p style="font-size: 0.9rem; margin-top: 10px;">Powered by LangGraph & Local LLMs</p>
    </div>
    """, unsafe_allow_html=True)

    # Main content area
    col1, col2, col3 = st.columns([2, 3, 1])

    with col1:
        st.markdown("### 🚀 Start Your Learning Journey")
        st.markdown("*Enter your study parameters below*")

    with st.form("study_form", clear_on_submit=False):
        col_form1, col_form2 = st.columns(2)

        with col_form1:
            topic_mode = st.radio(
                "📌 Topic Selection",
                ["Supported Topics", "Custom Topic"],
                horizontal=True,
            )

            selected_file = None

            if topic_mode == "Supported Topics":
                selected_topic = st.selectbox(
                    "Select a topic",
                    list(SUPPORTED_TOPICS.keys()),
                    key="dropdown_topic"
                )
                topic = selected_topic
                selected_file = SUPPORTED_TOPICS[selected_topic]

            else:
                st.info("💡 Custom topics will use LLM fallback if no notes file is found.")
                custom_topic = st.text_input(
                    "Enter your topic",
                    placeholder="e.g., Neural Networks",
                    key="custom_topic"
                )
                topic = custom_topic.strip()

        with col_form2:
            time_minutes = st.number_input(
                "⏱️ Available Time",
                min_value=5,
                max_value=180,
                value=30,
                step=5,
                help="How much time do you have for this study session?"
            )

            difficulty = st.select_slider(
                "📊 Difficulty Level",
                options=["easy", "medium", "hard"],
                value="medium",
                help="Choose based on your comfort with the topic"
            )

        submitted = st.form_submit_button("🎯 Generate Study Session", use_container_width=True)

    if submitted:
        if not topic.strip():
            st.error("⚠️ Please enter or select a topic to continue.")
            return

        with st.spinner("🔄 Initializing multi-agent system..."):
            notes_file_path, notes_found = resolve_notes_file(topic, selected_file)

            st.session_state["notes_found"] = notes_found
            st.session_state["notes_path"] = notes_file_path
            st.session_state["selected_topic"] = topic
            st.session_state["session_start_time"] = datetime.now()

            initial_state = build_initial_state(
                topic=topic,
                time_minutes=int(time_minutes),
                difficulty=difficulty,
                notes_file_path=notes_file_path,
            )

            # Show progress
            progress_bar = st.progress(0)
            status_text = st.empty()

            status_text.text("📋 Creating study plan...")
            progress_bar.progress(20)

            graph = build_full_graph()
            result = graph.invoke(initial_state)

            status_text.text("📚 Generating learning content...")
            progress_bar.progress(50)

            st.session_state["result"] = result
            st.session_state["quiz_generated"] = True
            st.session_state["answers_submitted"] = False

            status_text.text("✍️ Preparing assessment...")
            progress_bar.progress(80)

            status_text.text("✅ Session ready!")
            progress_bar.progress(100)

            st.rerun()

    # Display session content if available
    if st.session_state["result"]:
        result = st.session_state["result"]

        # Sidebar with session info
        render_sidebar_info(
            st.session_state.get("selected_topic", ""),
            result.get("difficulty", "medium"),
            result.get("time_minutes", 30),
            st.session_state.get("notes_found", False)
        )

        # Progress indicator
        if not st.session_state["answers_submitted"]:
            render_progress_bar("Learn")
        else:
            render_progress_bar("Evaluate")

        # Session content
        if st.session_state["notes_found"]:
            st.info(f"📄 Using local study materials from: `{st.session_state['notes_path']}`")
        else:
            st.info("🌐 Generating content using LLM knowledge base (no local notes found)")

        render_study_plan(result["study_plan"])
        render_lesson(result["lesson_content"])

        answers = render_quiz(result["quiz_questions"])

        col_btn1, col_btn2, col_btn3 = st.columns([1, 2, 1])
        with col_btn2:
            if st.button("✅ Submit Answers for Evaluation", use_container_width=True):
                with st.spinner("📊 Analyzing your responses..."):
                    result["student_answers"] = answers
                    graph = build_full_graph()
                    updated_result = graph.invoke(result)
                    st.session_state["result"] = updated_result
                    st.session_state["answers_submitted"] = True
                    save_result(updated_result)
                    st.rerun()

    if st.session_state["result"] and st.session_state["answers_submitted"]:
        result = st.session_state["result"]
        render_evaluation(result["evaluation_result"])
        render_logs(result["logs"])

        # Download button for session report
        if st.button("📥 Download Session Report", use_container_width=True):
            save_result(result)
            st.success("✅ Report saved to outputs/session_reports/")

    # Footer
    st.markdown("---")
    st.markdown(
        "<div style='text-align: center; color: #6c757d; font-size: 0.85rem;'>"
        "ExamPrep MAS | Multi-Agent System for Intelligent Learning | Powered by LangGraph & Ollama"
        "</div>",
        unsafe_allow_html=True
    )


if __name__ == "__main__":
    main()