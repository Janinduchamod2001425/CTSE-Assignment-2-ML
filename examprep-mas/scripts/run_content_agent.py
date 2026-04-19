# from agents.content_agent import content_agent

# def main():
#     # 🔹 Mock state (simulate planner output)
#     state = {
#         "topic": "Machine Learning",
#         "time_minutes": 30,
#         "difficulty": "easy",
#         "study_plan": [
#             "Introduction to Machine Learning",
#             "Core concepts of Machine Learning",
#             "Worked examples of Machine Learning",
#             "Quick revision of Machine Learning",
#         ],
#         "lesson_content": "",
#         "logs": []
#     }

#     result = content_agent(state)

#     print("\n=== CONTENT AGENT OUTPUT ===\n")
#     print(result["lesson_content"])

#     print("\n=== LOGS ===\n")
#     print(result["logs"])


# if __name__ == "__main__":
#     main()

#new one
import json
import os

from agents.content_agent import content_agent


def main():
    # 🔹 Get project root path (IMPORTANT)
    BASE_DIR = os.path.dirname(os.path.dirname(__file__))

    # 🔹 Load mock state from JSON file
    json_path = os.path.join(BASE_DIR, "data", "notes", "sample_inputs", "mock_state.json")

    with open(json_path, "r", encoding="utf-8") as f:
        state = json.load(f)

    # 🔹 Run content agent
    result = content_agent(state)

    print("\n=== CONTENT AGENT OUTPUT ===\n")
    print(result["lesson_content"])

    print("\n=== LOGS ===\n")
    print(result["logs"])


if __name__ == "__main__":
    main()