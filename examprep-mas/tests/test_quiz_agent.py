# test_quiz_agent.py

from agents.quiz_agent import quiz_agent


def build_quiz_state():
    return {
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


# -------------------------------------
# 1. BASIC FUNCTIONAL TEST
# -------------------------------------
def test_quiz_agent_generates_quiz_questions():
    state = build_quiz_state()
    result = quiz_agent(state)

    assert "quiz_questions" in result
    assert isinstance(result["quiz_questions"], list)
    assert len(result["quiz_questions"]) > 0


# -------------------------------------
# 2. ANSWER KEY GENERATION TEST
# -------------------------------------
def test_quiz_agent_generates_answer_key():
    state = build_quiz_state()
    result = quiz_agent(state)

    assert "answer_key" in result
    assert isinstance(result["answer_key"], list)
    assert len(result["answer_key"]) > 0


# -------------------------------------
# 3. QUESTION COUNT TEST
# -------------------------------------
def test_quiz_agent_respects_num_quiz_questions():
    state = build_quiz_state()
    state["num_quiz_questions"] = 3

    result = quiz_agent(state)

    assert len(result["quiz_questions"]) == 3
    assert len(result["answer_key"]) == 3


# -------------------------------------
# 4. QUESTION STRUCTURE TEST
# -------------------------------------
def test_quiz_question_structure():
    state = build_quiz_state()
    result = quiz_agent(state)

    for question in result["quiz_questions"]:
        assert isinstance(question, dict)
        assert "question" in question
        assert "type" in question
        assert isinstance(question["question"], str)
        assert question["question"].strip() != ""
        assert question["type"] in ["mcq", "short_answer", "mixed"] or isinstance(question["type"], str)

        if question["type"] == "mcq":
            assert "options" in question
            assert isinstance(question["options"], list)
            assert len(question["options"]) > 0


# -------------------------------------
# 5. ANSWER KEY STRUCTURE TEST
# -------------------------------------
def test_answer_key_structure():
    state = build_quiz_state()
    result = quiz_agent(state)

    for answer in result["answer_key"]:
        assert isinstance(answer, dict) or isinstance(answer, str)


# -------------------------------------
# 6. MCQ MODE TEST
# -------------------------------------
def test_quiz_agent_mcq_mode():
    state = build_quiz_state()
    state["question_type_mode"] = "mcq"

    result = quiz_agent(state)

    assert len(result["quiz_questions"]) > 0
    for question in result["quiz_questions"]:
        assert question["type"] == "mcq"
        assert "options" in question
        assert isinstance(question["options"], list)
        assert len(question["options"]) > 0


# -------------------------------------
# 7. SHORT ANSWER MODE TEST
# -------------------------------------
def test_quiz_agent_short_answer_mode():
    state = build_quiz_state()
    state["question_type_mode"] = "short_answer"

    result = quiz_agent(state)

    assert len(result["quiz_questions"]) > 0
    for question in result["quiz_questions"]:
        assert question["type"] == "short_answer"


# -------------------------------------
# 8. LOGGING VALIDATION
# -------------------------------------
def test_quiz_agent_logs_are_added():
    state = build_quiz_state()
    result = quiz_agent(state)

    assert "logs" in result
    assert isinstance(result["logs"], list)
    assert len(result["logs"]) > 0

    quiz_logs = [log for log in result["logs"] if log.get("agent") == "quiz_agent"]
    assert len(quiz_logs) > 0


# -------------------------------------
# 9. STATE UPDATE TEST
# -------------------------------------
def test_quiz_agent_updates_state_without_removing_existing_fields():
    state = build_quiz_state()
    result = quiz_agent(state)

    assert result["topic"] == state["topic"]
    assert result["difficulty"] == state["difficulty"]
    assert result["lesson_content"] == state["lesson_content"]
    assert isinstance(result["quiz_questions"], list)
    assert isinstance(result["answer_key"], list)


# -------------------------------------
# 10. EMPTY LESSON CONTENT SAFETY TEST
# -------------------------------------
def test_quiz_agent_handles_empty_lesson_content():
    state = build_quiz_state()
    state["lesson_content"] = ""

    result = quiz_agent(state)

    assert "quiz_questions" in result
    assert isinstance(result["quiz_questions"], list)
    assert "answer_key" in result
    assert isinstance(result["answer_key"], list)