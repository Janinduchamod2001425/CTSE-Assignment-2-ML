from agents.content_agent import content_agent
# from agents.planner_agent import planner_agent
# from agents.quiz_agent import quiz_agent
# from agents.evaluator_agent import evaluator_agent


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
    # Content Agent (YOUR PART)
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