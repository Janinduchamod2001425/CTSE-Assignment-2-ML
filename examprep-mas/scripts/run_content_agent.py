from agents.content_agent import content_agent

def main():
    # 🔹 Mock state (simulate planner output)
    state = {
        "topic": "Machine Learning",
        "time_minutes": 30,
        "difficulty": "medium",
        "study_plan": [
            "Introduction to Machine Learning",
            "Core concepts of Machine Learning",
            "Worked examples of Machine Learning",
            "Quick revision of Machine Learning",
        ],
        "lesson_content": "",
        "logs": []
    }

    result = content_agent(state)

    print("\n=== CONTENT AGENT OUTPUT ===\n")
    print(result["lesson_content"])

    print("\n=== LOGS ===\n")
    print(result["logs"])


if __name__ == "__main__":
    main()