from typing import List, Dict


def calculate_score(
    correct_answers: List[str],
    student_answers: List[str]
) -> int:
    """
    Calculate score by comparing correct and student answers.

    Args:
        correct_answers: list of correct answers
        student_answers: list of user answers

    Returns:
        score (int)
    """
    score = 0

    for correct, student in zip(correct_answers, student_answers):
        if student.strip().lower() == correct.strip().lower():
            score += 1

    return score