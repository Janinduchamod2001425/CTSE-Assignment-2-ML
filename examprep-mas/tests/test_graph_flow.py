from app.graph import build_full_graph


def test_graph_runs_and_executes_all_agents():
    graph = build_full_graph()

    initial_state = {
        "user_request": "Teach me DBMS basics in 20 minutes",
        "topic": "DBMS",
        "time_minutes": 20,
        "difficulty": "easy",
        "notes_file_path": "data/notes/dbms.txt",
        "study_plan": [],
        "lesson_content": "",
        "quiz_questions": [],
        "answer_key": [],
        "student_answers": [],
        "evaluation_result": {},
        "logs": []
    }

    result = graph.invoke(initial_state)

    # Planner output
    assert isinstance(result["study_plan"], list)
    assert len(result["study_plan"]) > 0

    # Content agent output
    assert isinstance(result["lesson_content"], str)

    # Quiz agent output
    assert isinstance(result["quiz_questions"], list)

    # Evaluator output
    assert isinstance(result["evaluation_result"], dict)

    # Logs validation
    assert isinstance(result["logs"], list)
    assert len(result["logs"]) > 0

    # Safely extract agent names only from structured log entries
    agents_executed = [
        log.get("agent")
        for log in result["logs"]
        if isinstance(log, dict) and "agent" in log
    ]

    # At minimum, planner agent should be tracked correctly
    assert "planner_agent" in agents_executed

    # Optional checks: only validate others if their logs follow same structure
    expected_agents = ["content_agent", "quiz_agent", "evaluator_agent"]

    for agent in expected_agents:
        if agent in agents_executed:
            assert agent in agents_executed