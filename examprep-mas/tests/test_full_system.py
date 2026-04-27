from agents.content_agent import content_agent
from agents.planner_agent import planner_agent
from agents.quiz_agent import quiz_agent
# from agents.quiz_agent import quiz_agent
# from agents.evaluator_agent import evaluator_agent


# -------------------------------------
# Planner Agent Test
# -------------------------------------
def test_full_pipeline_planner_agent_contribution():
    # =========================
    # Initial Shared State
    # =========================
    state = {
        "user_request": "Study Machine Learning in 30 minutes",
        "topic": "Machine Learning",
        "time_minutes": 30,
        "difficulty": "medium",
        "notes_file_path": "data/notes/ml.txt",
        "study_plan": [],
        "lesson_content": "",
        "quiz_questions": [],
        "answer_key": [],
        "student_answers": [],
        "evaluation_result": {},
        "logs": []
    }

    # =========================
    # Planner Agent (Janindu's PART)
    # =========================
    state = planner_agent(state)

    output = state["study_plan"]

    # -------------------------
    # Test Case 1: Study Plan Generation
    # -------------------------
    assert isinstance(output, list)
    assert len(output) > 0

    # -------------------------
    # Test Case 2: Step Limit Validation
    # -------------------------
    assert len(output) <= 5

    # -------------------------
    # Test Case 3: Step Type Validation
    # -------------------------
    assert all(isinstance(step, str) for step in output)

    # -------------------------
    # Test Case 4: No Empty Steps
    # -------------------------
    assert all(step.strip() != "" for step in output)

    # -------------------------
    # Test Case 5: Logging Check
    # -------------------------
    assert len(state["logs"]) > 0
    assert state["logs"][0]["agent"] == "planner_agent"
    assert state["logs"][0]["tool_called"] == "create_study_plan"
    assert state["logs"][0]["status"] == "success"

    # -------------------------
    # Test Case 6: State Update Check
    # -------------------------
    assert "study_plan" in state
    assert isinstance(state["study_plan"], list)


# -------------------------------------
# Content Agent Test
# -------------------------------------
def test_full_pipeline_content_agent():

    # =========================
    # Initial Shared State
    # =========================
    state = {
        "topic": "Machine Learning",
        "time_minutes": 30,
        "difficulty": "easy",

        # Planner will normally fill this,
        # but for now we simulate it (since we focus on Content Agent)
        "study_plan": [
            "Introduction to Machine Learning",
            "Core concepts of Machine Learning",
            "Worked examples of Machine Learning",
            "Quick revision of Machine Learning"
        ],

        "lesson_content": "",
        "quiz_questions": [],
        "answer_key": [],
        "student_answers": [],
        "evaluation_result": {},
        "logs": []
    }

    # =========================
    # Content Agent (Sachin's PART)
    # =========================
    state = content_agent(state)

    output = state["lesson_content"]

    # -------------------------
    # Test Case 1: Content Generation
    # -------------------------
    assert len(output) > 0
    assert "# Topic:" in output

    # -------------------------
    # Test Case 2: Structure Validation
    # -------------------------
    assert "## 1." in output or "Section 1" in output
    assert "Summary" in output

    # -------------------------
    # Test Case 3: Difficulty Handling
    # -------------------------
    assert state["difficulty"] in ["easy", "medium", "hard"]

    # -------------------------
    # Test Case 4: Time Constraint Handling
    # -------------------------
    assert state["time_minutes"] > 0

    # -------------------------
    # Test Case 5: Content Quality (Basic)
    # -------------------------
    assert len(output) > 50

    # -------------------------
    # Test Case 6: Logging Check
    # -------------------------
    assert len(state["logs"]) > 0

    # -------------------------
    # Test Case 7: No External Knowledge Keywords
    # -------------------------
    forbidden_words = ["Wikipedia", "Google", "external source", "internet"]
    for word in forbidden_words:
        assert word.lower() not in output.lower()


    # =========================
    # Future Integration (Other Members)
    # =========================

    # Planner Agent
    # state = planner_agent(state)
    # assert len(state["study_plan"]) > 0

    # Quiz Agent
    # state = quiz_agent(state)
    # assert len(state["quiz_questions"]) > 0

    # Evaluator Agent
    # state = evaluator_agent(state)
    # assert "score" in state["evaluation_result"]

# -------------------------------------
# Quiz Agent Test
# -------------------------------------
def test_full_pipeline_quiz_agent():
    state = {
        "user_request": "Study Machine Learning in 30 minutes",
        "topic": "Machine Learning",
        "time_minutes": 30,
        "difficulty": "medium",
        "notes_file_path": "data/notes/ml.txt",
        "study_plan": [
            "Introduction to Machine Learning",
            "Core concepts of Machine Learning",
            "Worked examples of Machine Learning",
            "Quick revision of Machine Learning"
        ],
        "lesson_content": (
            "# Topic: Machine Learning\n\n"
            "## 1. Introduction\n"
            "Machine Learning is a field of AI that enables systems to learn from data.\n\n"
            "## 2. Core Concepts\n"
            "Supervised learning, unsupervised learning, and reinforcement learning are major types.\n\n"
            "## 3. Applications\n"
            "It is used in classification, recommendation systems, and image recognition.\n\n"
            "Summary: Machine Learning helps computers learn patterns from data."
        ),
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

    state = quiz_agent(state)

    assert "quiz_questions" in state
    assert isinstance(state["quiz_questions"], list)
    assert len(state["quiz_questions"]) > 0

    assert "answer_key" in state
    assert isinstance(state["answer_key"], list)
    assert len(state["answer_key"]) > 0

    assert len(state["quiz_questions"]) == 5
    assert len(state["answer_key"]) == 5

    for q in state["quiz_questions"]:
        assert isinstance(q, dict)
        assert "question" in q
        assert "type" in q
        assert isinstance(q["question"], str)
        assert q["question"].strip() != ""

        if q["type"] == "mcq":
            assert "options" in q
            assert isinstance(q["options"], list)
            assert len(q["options"]) > 0

    assert len(state["logs"]) > 0
    quiz_logs = [log for log in state["logs"] if log.get("agent") == "quiz_agent"]
    assert len(quiz_logs) > 0


# -------------------------------------
# Full Integration up to Quiz Agent
# -------------------------------------
def test_full_pipeline_planner_content_quiz_integration():
    state = {
        "user_request": "Study Machine Learning in 30 minutes",
        "topic": "Machine Learning",
        "time_minutes": 30,
        "difficulty": "medium",
        "notes_file_path": "data/notes/ml.txt",
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

    state = planner_agent(state)
    assert len(state["study_plan"]) > 0

    state = content_agent(state)
    assert len(state["lesson_content"]) > 0

    state = quiz_agent(state)
    assert len(state["quiz_questions"]) > 0
    assert len(state["answer_key"]) > 0



# -------------------------------------
# Evaluator Agent Test
# -------------------------------------