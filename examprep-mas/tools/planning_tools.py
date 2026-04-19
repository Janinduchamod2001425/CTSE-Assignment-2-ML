from typing import List


def create_study_plan(topic: str, minutes: int, difficulty: str) -> List[str]:
    """
    Create a simple ordered study plan for the requested topic.

    Args:
        topic: Study topic provided by the user.
        minutes: Available study time in minutes.
        difficulty: Requested difficulty level.

    Returns:
        A list of study plan steps.

    Raises:
        ValueError: If minutes is less than or equal to zero.
    """
    if minutes <= 0:
        raise ValueError("minutes must be greater than 0")

    difficulty = difficulty.lower().strip()

    plan = [f"Introduction to {topic}"]

    if minutes >= 15:
        plan.append(f"Core concepts of {topic}")

    if minutes >= 25:
        plan.append(f"Worked examples of {topic}")

    if difficulty == "hard" and minutes >= 35:
        plan.append(f"Advanced concepts of {topic}")

    plan.append(f"Quick revision of {topic}")

    return plan