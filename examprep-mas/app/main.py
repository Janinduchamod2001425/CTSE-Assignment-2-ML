from app.graph import build_prep_graph, build_quiz_graph
from agents.evaluator_agent import evaluator_agent
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

        # asked later
        "num_quiz_questions": 5,
        "quiz_level": "intermediate",
        "quiz_style": "practice",
        "question_type_mode": "mixed",

        "study_plan": [],
        "lesson_content": "",
        "quiz_questions": [],
        "answer_key": [],
        "student_answers": [],
        "evaluation_result": {},
        "logs": []
    }


def get_quiz_preferences():
    print("\n===== QUIZ SETTINGS =====")

    try:
        num_quiz_questions = int(input("How many quiz questions do you want? ").strip())
    except ValueError:
        num_quiz_questions = 5

    quiz_level = input(
        "Select quiz level (basic/intermediate/difficult): "
    ).strip().lower()

    quiz_style = input(
        "Select quiz style (exam/practice/revision/challenge): "
    ).strip().lower()

    question_type_mode = input(
        "Select question type (mixed/mcq/short_answer): "
    ).strip().lower()

    if num_quiz_questions <= 0:
        num_quiz_questions = 5

    if quiz_level not in {"basic", "intermediate", "difficult"}:
        quiz_level = "intermediate"

    if quiz_style not in {"exam", "practice", "revision", "challenge"}:
        quiz_style = "practice"

    if question_type_mode not in {"mixed", "mcq", "short_answer"}:
        question_type_mode = "mixed"

    return {
        "num_quiz_questions": num_quiz_questions,
        "quiz_level": quiz_level,
        "quiz_style": quiz_style,
        "question_type_mode": question_type_mode,
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
        print(f"\nQ{i}: {q['question']}")
        print(f"Type: {q['type']}")
        print(f"Level: {q.get('level', '-')}")
        if q["type"] == "mcq":
            for j, option in enumerate(q["options"], start=1):
                print(f"  {j}. {option}")
        if q.get("hint"):
            print(f"Hint: {q['hint']}")


def collect_answers(questions):
    print("\n✍️ Enter Your Answers:")
    answers = []

    for i, q in enumerate(questions, 1):
        if q["type"] == "mcq":
            ans = input(f"Answer for Q{i} (option number or text): ").strip()
            if ans.isdigit():
                index = int(ans) - 1
                if 0 <= index < len(q["options"]):
                    ans = q["options"][index]
            answers.append(ans)
        else:
            ans = input(f"Answer for Q{i}: ").strip()
            answers.append(ans)

    return answers


def print_evaluation(result):
    print("\n📊 Evaluation:")
    print(f"Score: {result.get('score')} / {result.get('total')}")
    print(f"Feedback: {result.get('feedback')}")


def print_logs(logs):
    print("\n🧾 Logs:")
    for log in logs:
        agent = log.get("agent", "unknown_agent")
        status = log.get("status", "executed")
        print(f"- {agent} executed ({status})")


# -------------------------------
# SAVE OUTPUT
# -------------------------------
def save_result(result):
    os.makedirs("outputs/session_reports", exist_ok=True)
    with open("outputs/session_reports/result.json", "w", encoding="utf-8") as f:
        json.dump(result, f, indent=4, ensure_ascii=False)


# -------------------------------
# MAIN EXECUTION
# -------------------------------
def main():
    prep_graph = build_prep_graph()
    quiz_graph = build_quiz_graph()

    # Step 1: initial input
    state = get_user_input()

    # Step 2: planner + content first
    state = prep_graph.invoke(state)

    # Step 3: show generated study content
    print("\n===== GENERATED STUDY SESSION =====")
    print_study_plan(state["study_plan"])
    print_lesson(state["lesson_content"])

    # Step 4: ask quiz settings after content
    quiz_prefs = get_quiz_preferences()
    state.update(quiz_prefs)

    # Step 5: generate quiz
    state = quiz_graph.invoke(state)

    # Step 6: show quiz
    print_quiz(state["quiz_questions"])

    # Step 7: collect answers
    answers = collect_answers(state["quiz_questions"])
    state["student_answers"] = answers

    # Step 8: evaluator only
    state = evaluator_agent(state)

    # Step 9: final output
    print("\n===== FINAL OUTPUT =====")
    print_evaluation(state["evaluation_result"])
    print_logs(state["logs"])

    # Step 10: save result
    save_result(state)


if __name__ == "__main__":
    main()