from agents.planner_agent import planner_agent


def test_planner_agent_updates_state_and_logs():
    initial_state = {
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

    result = planner_agent(initial_state)

    assert isinstance(result["study_plan"], list)
    assert len(result["study_plan"]) > 0
    assert len(result["logs"]) == 1
    assert result["logs"][0]["agent"] == "planner_agent"
    assert result["logs"][0]["tool_called"] == "create_study_plan"
    assert result["logs"][0]["status"] == "success"