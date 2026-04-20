from app.graph import build_graph


def test_graph_runs_and_executes_all_agents():
    graph = build_graph()

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
    assert len(result["logs"]) >= 4

    agents_executed = [log["agent"] for log in result["logs"]]

    assert "planner_agent" in agents_executed
    assert "content_agent" in agents_executed
    assert "quiz_agent" in agents_executed
    assert "evaluator_agent" in agents_executed