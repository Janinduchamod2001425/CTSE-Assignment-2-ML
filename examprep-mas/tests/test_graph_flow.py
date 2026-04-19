from app.graph import build_graph


def test_graph_runs_and_returns_study_plan():
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

    assert isinstance(result["study_plan"], list)
    assert len(result["study_plan"]) > 0
    assert len(result["logs"]) > 0