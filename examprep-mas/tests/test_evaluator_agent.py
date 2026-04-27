from agents.evaluator_agent import evaluator_agent


def test_evaluator_basic():
    state = {
        "topic": "ML",
        "quiz_questions": [
            {"type": "mcq", "question": "Q1"},
            {"type": "short_answer", "question": "Q2"}
        ],
        "answer_key": [
            {"correct_answer": "A"},
            {"correct_answer": "Machine Learning is AI"}
        ],
        "student_answers": ["A", "Machine Learning is AI"],
        "logs": []
    }

    result = evaluator_agent(state)

    assert result["evaluation_result"]["score"] == 2
    assert result["evaluation_result"]["total"] == 2