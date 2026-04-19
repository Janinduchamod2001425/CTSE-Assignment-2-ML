from agents.planner_agent import planner_agent

initial_state = {
    "user_request": "Teach me machine learning basics in 30 minutes",
    "topic": "Machine Learning",
    "time_minutes": 30,
    "difficulty": "medium",
    "notes_file_path": "data/notes/machine_learning.txt",
    "study_plan": [],
    "lesson_content": "",
    "quiz_questions": [],
    "answer_key": [],
    "student_answers": [],
    "evaluation_result": {},
    "logs": []
}


def main():
    result = planner_agent(initial_state)
    print("Planner Agent Output:")
    print(result["study_plan"])
    print("\nLogs:")
    print(result["logs"])


if __name__ == "__main__":
    main()