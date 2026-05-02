import os
import json
import streamlit as st
import matplotlib.pyplot as plt

from datetime import datetime

from app.graph import build_prep_graph, build_quiz_graph
from agents.evaluator_agent import evaluator_agent

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
            padding: 10px;
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
            background: linear-gradient(135deg, #2d3748 0%, #1a202c 100%);
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
            color: #f7fafc;
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
            color: #2c3e50;
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

        /* ========== PLANNER ENHANCED STYLES ========== */

        /* Planner Dashboard */
        .planner-dashboard {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            border-radius: 24px;
            padding: 20px;
            margin-bottom: 30px;
            box-shadow: 0 20px 40px rgba(0,0,0,0.1);
        }

        /* Stat Cards */
        .planner-stat-card {
            background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
            border-radius: 16px;
            border: 1px solid #e9ecef;
            padding: 10px;
            text-align: center;
            backdrop-filter: blur(10px);
            transition: transform 0.3s ease;
        }

        .planner-stat-card:hover {
            transform: translateY(-5px);
        }

        .stat-icon {
            font-size: 2rem;
            margin-bottom: 8px;
        }

        .stat-value {
            font-size: 1.8rem;
            font-weight: 700;
            color: #667eea;
        }

        .stat-label {
            font-size: 0.85rem;
            color: #fffffe;
            margin-top: 5px;
        }

        /* Timeline */
        .planner-timeline-header {
            background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
            padding: 20px;
            border-radius: 16px;
            margin: 20px 0;
        }

        .planner-timeline-header h3 {
            margin: 0;
            color: white;
        }

        .planner-timeline-header p {
            margin: 5px 0 0;
            color: gray;
        }

        /* Modern Timeline Item Styles */
        .planner-timeline-item {
            display: flex;
            margin-bottom: 30px;
            position: relative;
        }
        
        .timeline-marker {
            width: 80px;
            position: relative;
            display: flex;
            flex-direction: column;
            align-items: center;
        }
        
        .timeline-circle {
            width: 48px;
            height: 48px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            position: relative;
            z-index: 2;
            box-shadow: 0 8px 20px rgba(102,126,234,0.4);
            transition: all 0.3s ease;
        }
        
        .timeline-circle:hover {
            transform: scale(1.1);
            box-shadow: 0 12px 28px rgba(102,126,234,0.6);
        }
        
        .circle-number {
            color: white;
            font-weight: 700;
            font-size: 1.2rem;
            position: relative;
            z-index: 2;
        }
        
        .circle-pulse {
            position: absolute;
            width: 100%;
            height: 100%;
            border-radius: 50%;
            background: rgba(102,126,234,0.6);
            animation: pulse 2s infinite;
            z-index: 1;
        }
        
        @keyframes pulse {
            0% {
                transform: scale(1);
                opacity: 0.6;
            }
            70% {
                transform: scale(1.3);
                opacity: 0;
            }
            100% {
                transform: scale(1.4);
                opacity: 0;
            }
        }
        
        .timeline-line {
            position: absolute;
            left: 50%;
            top: 48px;
            width: 2px;
            height: calc(100% + 30px);
            background: linear-gradient(180deg, #667eea 0%, rgba(102,126,234,0.2) 100%);
            transform: translateX(-50%);
        }
        
        .planner-timeline-item:last-child .timeline-line {
            display: none;
        }
        
        /* Timeline Content - Glassmorphism Card */
        .timeline-content {
            flex: 1;
            background: rgba(255,255,255,0.03);
            backdrop-filter: blur(10px);
            border-radius: 20px;
            padding: 24px;
            margin-left: 20px;
            border: 1px solid rgba(255,255,255,0.1);
            transition: all 0.3s ease;
            position: relative;
            overflow: hidden;
        }
        
        .timeline-content::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 3px;
            background: linear-gradient(90deg, #667eea, #764ba2, #667eea);
            transform: translateX(-100%);
            transition: transform 0.5s ease;
        }
        
        .timeline-content:hover::before {
            transform: translateX(0);
        }
        
        .timeline-content:hover {
            transform: translateX(8px);
            background: rgba(255,255,255,0.05);
            border-color: rgba(102,126,234,0.3);
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
        }
        
        .timeline-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 16px;
            flex-wrap: wrap;
            gap: 12px;
        }
        
        .step-badge {
            background: linear-gradient(135deg, rgba(102,126,234,0.2), rgba(118,75,162,0.2));
            padding: 6px 14px;
            border-radius: 30px;
            font-size: 0.75rem;
            font-weight: 700;
            letter-spacing: 1px;
            color: #667eea;
            border: 1px solid rgba(102,126,234,0.3);
            backdrop-filter: blur(5px);
        }
        
        .badge-icon {
            margin-right: 6px;
            font-size: 0.85rem;
        }
        
        .step-time {
            display: flex;
            align-items: center;
            gap: 6px;
            background: rgba(0,0,0,0.3);
            padding: 6px 12px;
            border-radius: 20px;
        }
        
        .time-icon {
            font-size: 2rem;
        }
        
        .time-value {
            color: rgba(255,255,255,0.9);
            font-size: 1rem;
            font-weight: 600;
        }
        
        .step-title {
            font-size: 1.15rem;
            font-weight: 600;
            color: rgba(255,255,255,0.95);
            margin-bottom: 16px;
            line-height: 1.4;
        }
        
        /* Meta Tags */
        .step-meta {
            display: flex;
            gap: 12px;
            flex-wrap: wrap;
            margin-bottom: 20px;
        }
        
        .meta-tag {
            display: flex;
            align-items: center;
            gap: 6px;
            background: rgba(255,255,255,0.05);
            padding: 4px 12px;
            border-radius: 20px;
            font-size: 0.75rem;
            color: rgba(255,255,255,0.7);
            border: 1px solid rgba(255,255,255,0.08);
            transition: all 0.2s ease;
        }
        
        .meta-tag:hover {
            background: rgba(102,126,234,0.2);
            border-color: rgba(102,126,234,0.3);
        }
        
        .meta-icon {
            font-size: 0.85rem;
        }
        
        /* Progress Bar */
        .step-progress {
            margin-bottom: 20px;
        }
        
        .progress-info {
            display: flex;
            justify-content: space-between;
            margin-bottom: 8px;
        }
        
        .progress-label {
            font-size: 0.75rem;
            color: rgba(255,255,255,0.5);
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }
        
        .progress-percent {
            font-size: 0.75rem;
            color: #667eea;
            font-weight: 600;
        }
        
        .progress-bar-bg {
            background: rgba(255,255,255,0.1);
            border-radius: 12px;
            height: 8px;
            overflow: hidden;
            position: relative;
        }
        
        .progress-bar-fill {
            background: linear-gradient(90deg, #667eea, #764ba2);
            height: 100%;
            border-radius: 12px;
            position: relative;
            transition: width 0.5s ease;
        }
        
        .progress-glow {
            position: absolute;
            top: 0;
            right: 0;
            width: 20px;
            height: 100%;
            background: linear-gradient(90deg, transparent, rgba(255,255,255,0.3));
            animation: shimmer 2s infinite;
        }
        
        @keyframes shimmer {
            0% {
                transform: translateX(-100%);
            }
            100% {
                transform: translateX(200%);
            }
        }
        
        /* Action Button */
        .step-action {
            margin-top: 16px;
        }
        
        .step-start-btn {
            background: linear-gradient(135deg, #667eea, #764ba2);
            border: none;
            padding: 8px 20px;
            border-radius: 30px;
            color: white;
            font-weight: 600;
            font-size: 0.85rem;
            cursor: pointer;
            transition: all 0.3s ease;
            display: inline-flex;
            align-items: center;
            gap: 8px;
            box-shadow: 0 4px 12px rgba(102,126,234,0.3);
        }
        
        .step-start-btn:hover {
            transform: translateX(5px);
            box-shadow: 0 6px 20px rgba(102,126,234,0.5);
            gap: 12px;
        }
        
        /* Suggestions Panel - Dark Theme */
        .suggestions-panel {
            background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
            border-radius: 20px;
            justify-content: center;
            padding: 20px 10px 0px 20px;
            margin: 20px 0;
            border: 1px solid rgba(255,255,255,0.1);
        }
        
        .suggestions-header {
            font-size: 1.2rem;
            font-weight: 700;
            margin-bottom: 15px;
            color: #ffffff;
        }
        
        .suggestions-icon {
            font-size: 1.5rem;
            margin-right: 10px;
        }
        
        .suggestions-grid {
            display: grid;
            gap: 12px;
        }
        
        .suggestion-item {
            display: flex;
            align-items: center;
            background: rgba(255,255,255,0.05);
            backdrop-filter: blur(10px);
            padding: 12px;
            margin-bottom: 8px;
            border-radius: 12px;
            transition: transform 0.2s ease;
            border: 1px solid rgba(255,255,255,0.08);
        }
        
        .suggestion-item:hover {
            transform: translateX(5px);
            background: rgba(255,255,255,0.08);
            border-color: rgba(102,126,234,0.3);
        }
        
        .suggestion-bullet {
            font-size: 1.2rem;
            margin-right: 12px;
        }
        
        .suggestion-text {
            color: rgba(255,255,255,0.85);
            font-size: 0.9rem;
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
        "prep_completed": False,
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
        "num_quiz_questions": 5,
        "quiz_level": "intermediate",
        "quiz_style": "practice",
        "question_type_mode": "mixed",
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


def render_enhanced_study_plan(plan: list[str], topic: str, difficulty: str, time_minutes: int) -> None:
    """Professional course-style study plan display"""

    st.markdown('<div class="planner-dashboard">', unsafe_allow_html=True)

    # Header with stats
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown("""
            <div class="planner-stat-card">
                <div class="stat-icon">📚</div>
                <div class="stat-value">""" + str(len(plan)) + """</div>
                <div class="stat-label">Learning Modules</div>
            </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
            <div class="planner-stat-card">
                <div class="stat-icon">⏱️</div>
                <div class="stat-value">{time_minutes}</div>
                <div class="stat-label">Minutes Total</div>
            </div>
        """, unsafe_allow_html=True)

    with col3:
        difficulty_emoji = {"easy": "🟢", "medium": "🟡", "hard": "🔴"}
        st.markdown(f"""
            <div class="planner-stat-card">
                <div class="stat-icon">{difficulty_emoji.get(difficulty, "📊")}</div>
                <div class="stat-value">{difficulty.upper()}</div>
                <div class="stat-label">Difficulty Level</div>
            </div>
        """, unsafe_allow_html=True)

    with col4:
        st.markdown("""
            <div class="planner-stat-card">
                <div class="stat-icon">🎯</div>
                <div class="stat-value">95%</div>
                <div class="stat-label">Success Rate</div>
            </div>
        """, unsafe_allow_html=True)

    # Timeline view
    st.markdown(f"""
        <div class="planner-timeline-header">
            <h3>📋 Your Learning Path</h3>
            <p>Mastering <strong>{topic}</strong> in {time_minutes} minutes</p>
        </div>
    """, unsafe_allow_html=True)

    # Interactive timeline
    for i, step in enumerate(plan, 1):
        # Estimate time per step
        step_time = max(5, int(time_minutes / len(plan)))

        st.markdown(f"""
            <div class="planner-timeline-item">
                <div class="timeline-marker">
                    <div class="timeline-circle">
                        <span class="circle-number">{i}</span>
                        <div class="circle-pulse"></div>
                    </div>
                    <div class="timeline-line"></div>
                </div>
                <div class="timeline-content">
                    <div class="timeline-header">
                        <div class="step-badge">
                            <span class="badge-icon">📌</span>
                            MODULE {i:02d}
                        </div>
                        <div class="step-time">
                            <span class="time-icon">⏱️</span>
                            <span class="time-value">{step_time} min</span>
                        </div>
                    </div>
                    <div class="step-title">{step}</div>
                    <div class="step-meta">
                        <div class="meta-tag">
                            <span class="meta-icon">🎯</span>
                            <span>Key Concept</span>
                        </div>
                        <div class="meta-tag">
                            <span class="meta-icon">📚</span>
                            <span>Interactive Learning</span>
                        </div>
                        <div class="meta-tag">
                            <span class="meta-icon">✅</span>
                            <span>Knowledge Check</span>
                        </div>
                    </div>
                </div>
            </div>
        """, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

def render_smart_suggestions(topic: str, difficulty: str) -> None:
    """AI-powered study suggestions"""

    st.markdown("""
        <div class="suggestions-panel">
            <div class="suggestions-header">
                <span class="suggestions-icon">🧠</span>
                <span>AI Study Tips</span>
            </div>
            <div class="suggestions-grid">
    """, unsafe_allow_html=True)

    tips = [
        "🎯 Focus on understanding concepts before memorization",
        "📝 Take notes of key terms you encounter",
        "⏰ Take a 2-minute break every 15 minutes",
        f"💡 Based on {difficulty} difficulty, expect challenging questions",
        "🔄 Review weak areas after the quiz"
    ]

    for tip in tips:
        st.markdown(f"""
            <div class="suggestion-item">
                <div class="suggestion-bullet">✨</div>
                <div class="suggestion-text">{tip}</div>
            </div>
        """, unsafe_allow_html=True)

    st.markdown('</div></div>', unsafe_allow_html=True)

def render_lesson(content: str) -> None:
    st.markdown('<div class="custom-card">', unsafe_allow_html=True)

    # Header
    st.markdown("""
        <div style="display:flex; align-items:center; justify-content:space-between;">
            <h3 style="margin:0;">📖 Learning Material</h3>
            <span style="
                background:#667eea;
                color:white;
                padding:4px 12px;
                border-radius:20px;
                font-size:0.8rem;
            ">
                AI Generated
            </span>
        </div>
        <p style="color:#6c757d; margin-top:5px;">
            Structured explanation based on your study plan
        </p>
    """, unsafe_allow_html=True)

    # Content display
    if len(content) > 500:
        with st.expander("📚 View Full Lesson Content", expanded=True):
            st.markdown(content)  # ✅ KEEP MARKDOWN (important)
    else:
        st.markdown(content)

    st.markdown('</div>', unsafe_allow_html=True)


def render_quiz(questions: list) -> list[str]:
    st.markdown('<div class="custom-card">', unsafe_allow_html=True)
    st.markdown("### ✍️ Knowledge Check")
    st.markdown("*Answer these questions to test your understanding*")

    answers: list[str] = []

    for i, q in enumerate(questions, 1):
        if isinstance(q, dict):
            question_text = q.get("question", "")
            question_type = q.get("type", "short_answer")
            level = q.get("level", "")
            options = q.get("options", [])
            hint = q.get("hint", "")
        else:
            question_text = str(q)
            question_type = "short_answer"
            level = ""
            options = []
            hint = ""

        st.markdown(f"""
        <div class="quiz-question">
            <div class="question-text">Question {i}</div>
            <div>{question_text}</div>
        </div>
        """, unsafe_allow_html=True)

        if level:
            st.caption(f"Level: {level}")

        if question_type == "mcq" and options:
            answer = st.radio(
                f"Choose your answer for Question {i}",
                options,
                key=f"answer_{i}",
                index=None
            )
            answers.append(answer if answer is not None else "")
        else:
            answer = st.text_area(
                f"Your Answer for Question {i}",
                key=f"answer_{i}",
                placeholder="Type your answer here...",
                height=100
            )
            answers.append(answer)

        if hint:
            st.caption(f"Hint: {hint}")

    st.markdown('</div>', unsafe_allow_html=True)
    return answers


# =========================
# EVALUATOR ANALYTICS HELPERS
# =========================

def get_grade(percentage):
    if percentage >= 85:
        return "A"
    elif percentage >= 70:
        return "B"
    elif percentage >= 50:
        return "C"
    else:
        return "D"


def render_score_chart(result):
    correct = result["score"]
    incorrect = result["total"] - result["score"]

    labels = ["Correct", "Incorrect"]
    values = [correct, incorrect]

    plt.figure()
    plt.pie(values, labels=labels, autopct='%1.1f%%')
    plt.title("Performance Distribution")

    st.pyplot(plt)


def render_difficulty_chart(detailed_results):
    stats = {}

    for item in detailed_results:
        level = item.get("level", "intermediate")
        stats.setdefault(level, [0, 0])
        stats[level][1] += 1

        if item.get("is_correct"):
            stats[level][0] += 1

    levels = []
    accuracy = []

    for level, (correct, total) in stats.items():
        levels.append(level)
        accuracy.append((correct / total) * 100)

    plt.figure()
    plt.bar(levels, accuracy)
    plt.ylabel("Accuracy %")
    plt.title("Performance by Difficulty")

    st.pyplot(plt)


def render_question_analysis(detailed_results):
    st.markdown("### 📊 Question Analysis")

    for i, item in enumerate(detailed_results, 1):
        if item["is_correct"]:
            st.success(f"Q{i} Correct")
        else:
            st.error(f"Q{i} Incorrect")
            st.write(f"Correct Answer: {item['correct_answer']}")


def render_evaluation(result: dict) -> None:
    st.markdown('<div class="custom-card">', unsafe_allow_html=True)
    st.markdown("### 📊 Performance Analysis")

    score = result.get('score', 0)
    total = result.get('total', 1)
    percentage = result.get('percentage', (score / total) * 100)

    grade = get_grade(percentage)

    # Score card
    st.markdown(f"""
    <div class="score-card">
        <div>Your Score</div>
        <div class="score-number">{score} / {total}</div>
        <div style="font-size: 1.2rem;">{percentage:.1f}%</div>
    </div>
    """, unsafe_allow_html=True)

    # Grade
    st.markdown(f"### 🎓 Grade: {grade}")

    # Progress bar
    st.progress(percentage / 100)

    # Charts
    render_score_chart(result)

    if "detailed_results" in result:
        render_difficulty_chart(result["detailed_results"])

    # Feedback
    if result.get("feedback"):
        st.markdown(f'<div class="feedback-text">💬 {result["feedback"]}</div>', unsafe_allow_html=True)

    # Weak areas
    if result.get("weak_areas"):
        st.markdown("### ⚠️ Areas for Improvement")
        for w in result["weak_areas"]:
            st.warning(w)

    # Suggestions
    if result.get("suggestions"):
        st.markdown("### 💡 Recommendations")
        for s in result["suggestions"]:
            st.success(s)

    # Question analysis
    if "detailed_results" in result:
        render_question_analysis(result["detailed_results"])

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
                    unsafe_allow_html=True
                )
            elif idx == current_index:
                st.markdown(
                    f'<div style="text-align:center"><span class="progress-step active">{idx + 1}</span><br>{step}</div>',
                    unsafe_allow_html=True
                )
            else:
                st.markdown(
                    f'<div style="text-align:center"><span class="progress-step">{idx + 1}</span><br>{step}</div>',
                    unsafe_allow_html=True
                )


def main() -> None:
    st.set_page_config(
        page_title="ExamPrep MAS - Intelligent Study Assistant",
        page_icon="🎓",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    apply_custom_css()
    initialize_session_state()

    st.markdown("""
    <div class="main-header">
        <h1>🎓 ExamPrep MAS</h1>
        <p>Multi-Agent System for Intelligent Exam Preparation</p>
        <p style="font-size: 0.9rem; margin-top: 10px;">Powered by LangGraph & Local LLMs</p>
    </div>
    """, unsafe_allow_html=True)

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

            progress_bar = st.progress(0)
            status_text = st.empty()

            status_text.text("📋 Creating study plan...")
            progress_bar.progress(30)

            prep_graph = build_prep_graph()
            result = prep_graph.invoke(initial_state)

            status_text.text("📚 Generating learning content...")
            progress_bar.progress(80)

            st.session_state["result"] = result
            st.session_state["prep_completed"] = True
            st.session_state["quiz_generated"] = False
            st.session_state["answers_submitted"] = False

            status_text.text("✅ Study content ready!")
            progress_bar.progress(100)

            st.rerun()

    if st.session_state["result"]:
        result = st.session_state["result"]

        render_sidebar_info(
            st.session_state.get("selected_topic", ""),
            result.get("difficulty", "medium"),
            result.get("time_minutes", 30),
            st.session_state.get("notes_found", False)
        )

        if not st.session_state["quiz_generated"]:
            render_progress_bar("Learn")
        elif not st.session_state["answers_submitted"]:
            render_progress_bar("Quiz")
        else:
            render_progress_bar("Evaluate")

        if st.session_state["notes_found"]:
            st.info(f"📄 Using local study materials from: `{st.session_state['notes_path']}`")
        else:
            st.info("🌐 Generating content using LLM knowledge base (no local notes found)")

        # Enhanced Planner Display
        if st.session_state["prep_completed"] and not st.session_state["quiz_generated"]:
            # Show enhanced planner with all features
            render_enhanced_study_plan(
                result["study_plan"],
                st.session_state.get("selected_topic", ""),
                result.get("difficulty", "medium"),
                result.get("time_minutes", 30)
            )

            # Add smart suggestions
            render_smart_suggestions(
                st.session_state.get("selected_topic", ""),
                result.get("difficulty", "medium")
            )
        else:
            # Standard view for later stages
            render_study_plan(result["study_plan"])

        render_lesson(result["lesson_content"])

        if st.session_state["prep_completed"] and not st.session_state["quiz_generated"]:
            st.markdown('<div class="custom-card">', unsafe_allow_html=True)
            st.markdown("### ✍️ Generate Quiz")
            st.markdown("*Choose your quiz preferences, then generate the quiz*")

            with st.form("quiz_settings_form", clear_on_submit=False):
                col_q1, col_q2 = st.columns(2)

                with col_q1:
                    num_quiz_questions = st.number_input(
                        "How many quiz questions do you want?",
                        min_value=1,
                        max_value=20,
                        value=int(result.get("num_quiz_questions", 5)),
                        step=1
                    )

                    quiz_level = st.selectbox(
                        "Select quiz level",
                        ["basic", "intermediate", "difficult"],
                        index=["basic", "intermediate", "difficult"].index(result.get("quiz_level", "intermediate"))
                        if result.get("quiz_level", "intermediate") in ["basic", "intermediate", "difficult"]
                        else 1
                    )

                with col_q2:
                    quiz_style = st.selectbox(
                        "Select quiz style",
                        ["exam", "practice", "revision", "challenge"],
                        index=["exam", "practice", "revision", "challenge"].index(result.get("quiz_style", "practice"))
                        if result.get("quiz_style", "practice") in ["exam", "practice", "revision", "challenge"]
                        else 1
                    )

                    question_type_mode = st.selectbox(
                        "Select question type",
                        ["mixed", "mcq", "short_answer"],
                        index=["mixed", "mcq", "short_answer"].index(result.get("question_type_mode", "mixed"))
                        if result.get("question_type_mode", "mixed") in ["mixed", "mcq", "short_answer"]
                        else 0
                    )

                quiz_submit = st.form_submit_button("✍️ Generate Quiz", use_container_width=True)

            st.markdown('</div>', unsafe_allow_html=True)

            if quiz_submit:
                with st.spinner("✍️ Generating quiz based on your selected options..."):
                    result["num_quiz_questions"] = int(num_quiz_questions)
                    result["quiz_level"] = quiz_level
                    result["quiz_style"] = quiz_style
                    result["question_type_mode"] = question_type_mode

                    quiz_graph = build_quiz_graph()
                    updated_result = quiz_graph.invoke(result)

                    st.session_state["result"] = updated_result
                    st.session_state["quiz_generated"] = True
                    st.session_state["answers_submitted"] = False
                    st.rerun()

        if st.session_state["quiz_generated"]:
            answers = render_quiz(result["quiz_questions"])

            col_btn1, col_btn2, col_btn3 = st.columns([1, 2, 1])
            with col_btn2:
                if st.button("Submit Answers for Evaluation", use_container_width=True):
                    with st.spinner("Analyzing your responses..."):
                        result["student_answers"] = answers
                        updated_result = evaluator_agent(result)
                        st.session_state["result"] = updated_result
                        st.session_state["answers_submitted"] = True
                        save_result(updated_result)
                        st.rerun()

    if st.session_state["result"] and st.session_state["answers_submitted"]:
        result = st.session_state["result"]
        render_evaluation(result["evaluation_result"])
        render_logs(result["logs"])

        if st.button("📥 Download Session Report", use_container_width=True):
            save_result(result)
            st.success("✅ Report saved to outputs/session_reports/")

    st.markdown("---")
    st.markdown(
        "<div style='text-align: center; color: #6c757d; font-size: 0.85rem;'>"
        "ExamPrep MAS | Multi-Agent System for Intelligent Learning | Powered by LangGraph & Ollama"
        "</div>",
        unsafe_allow_html=True
    )


if __name__ == "__main__":
    main()