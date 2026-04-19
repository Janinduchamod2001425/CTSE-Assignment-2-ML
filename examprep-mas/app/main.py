from app.graph import build_graph
import json
import os


# -------------------------------
# USER INPUT SECTION
# -------------------------------
def get_user_input():
    print("\n===== ExamPrep MAS =====")

    topic = input("Enter Topic: ").strip()
    time_minutes = int(input("Enter Available Time (minutes): ").strip())
    difficulty = input("Enter Difficulty (easy/medium/hard): ").strip().lower()
    notes_file = input("Enter notes file name (e.g., machine_learning.txt): ").strip()

    return {
        "user_request": f"Study {topic} in {time_minutes} minutes",
        "topic": topic,
        "time_minutes": time_minutes,
        "difficulty": difficulty,
        "notes_file_path": f"data/notes/{notes_file}",
        "study_plan": [],
        "lesson_content": "",
        "quiz_questions": [],
        "answer_key": [],
        "student_answers": [],
        "evaluation_result": {},
        "logs": []
    }


# -------------------------------
# PRINT FUNCTIONS
# -------------------------------
def print_study_plan(plan):
    print("\n📘 Study Plan:")
    for i, step in enumerate(plan, 1):
        print(f"{i}. {step}")


def print_lesson(content):
    print("\n📖 Lesson Content:")
    print(content)


def print_quiz(questions):
    print("\n📝 Quiz:")
    for i, q in enumerate(questions, 1):
        print(f"Q{i}: {q}")


def collect_answers(questions):
    print("\n✍️ Enter Your Answers:")
    answers = []
    for i, q in enumerate(questions, 1):
        ans = input(f"Answer for Q{i}: ")
        answers.append(ans)
    return answers


def print_evaluation(result):
    print("\n📊 Evaluation:")
    print(f"Score: {result.get('score')} / {result.get('total')}")
    print(f"Feedback: {result.get('feedback')}")


def print_logs(logs):
    print("\n🧾 Logs:")
    for log in logs:
        print(f"- {log['agent']} executed")


# -------------------------------
# SAVE OUTPUT (OPTIONAL)
# -------------------------------
def save_result(result):
    os.makedirs("outputs/session_reports", exist_ok=True)
    with open("outputs/session_reports/result.json", "w") as f:
        json.dump(result, f, indent=4)


# -------------------------------
# MAIN EXECUTION
# -------------------------------
def main():
    graph = build_graph()

    # Step 1: Get user input
    state = get_user_input()

    # Step 2: Run pipeline (Planner → Content → Quiz → Evaluator)
    result = graph.invoke(state)

    # Step 3: Show results BEFORE answering
    print("\n===== GENERATED SESSION =====")
    print_study_plan(result["study_plan"])
    print_lesson(result["lesson_content"])
    print_quiz(result["quiz_questions"])

    # Step 4: Collect student answers
    answers = collect_answers(result["quiz_questions"])
    result["student_answers"] = answers

    # Step 5: Re-run ONLY evaluator
    # (Important: simulate second stage evaluation)
    result = graph.invoke(result)

    # Step 6: Final evaluation output
    print("\n===== FINAL OUTPUT =====")
    print_evaluation(result["evaluation_result"])
    print_logs(result["logs"])

    # Step 7: Save result (optional but HIGH VALUE)
    save_result(result)


if __name__ == "__main__":
    main()