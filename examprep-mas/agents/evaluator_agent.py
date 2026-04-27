from typing import Dict, Any, List
import ollama
import json


# =========================
# SMART RECOMMENDATION LOGIC
# =========================
def _generate_smart_recommendations(
    score: int,
    total: int,
    weak_areas: List[str],
    difficulty_stats: Dict[str, Dict[str, int]]
) -> List[str]:
    percentage = (score / total) * 100 if total > 0 else 0

    suggestions = []

    # Overall performance based suggestions
    if percentage >= 85:
        suggestions.append("Try advanced level questions to further challenge yourself")
        suggestions.append("Explore real-world applications of this topic")
        suggestions.append("Attempt more difficult quiz styles for stronger mastery")
    elif percentage >= 60:
        suggestions.append("Practice more questions to strengthen understanding")
        suggestions.append("Review important concepts you are unsure about")
        suggestions.append("Focus on improving accuracy in medium and difficult questions")
    else:
        suggestions.append("Revisit fundamental concepts before attempting more questions")
        suggestions.append("Spend more time studying the basics")
        suggestions.append("Go through lesson content again before retrying the quiz")

    # Weak-area-based suggestions
    if weak_areas:
        suggestions.append("Focus on incorrect questions and understand your mistakes")
        suggestions.append("Revise topics related to your weak areas")

    # Difficulty-level-based suggestions
    for level, stats in difficulty_stats.items():
        if stats["total"] > 0:
            accuracy = (stats["correct"] / stats["total"]) * 100
            if accuracy < 50:
                suggestions.append(f"You need more practice in {level} level questions")

    # Remove duplicates while keeping order
    unique_suggestions = []
    seen = set()
    for item in suggestions:
        if item not in seen:
            unique_suggestions.append(item)
            seen.add(item)

    return unique_suggestions


# =========================
# Helpers
# =========================
def _normalize_answer(text: str) -> str:
    return str(text).strip().lower()


# =========================
# GRADING LOGIC (UPGRADED)
# =========================
def _basic_grading(
    questions: List[Dict[str, Any]],
    answers: List[str],
    answer_key: List[Dict[str, Any]]
):
    score = 0
    total = len(answer_key)

    weak_areas = []
    detailed_results = []

    for i, (q, student_ans, key) in enumerate(zip(questions, answers, answer_key)):
        correct = key["correct_answer"]
        level = q.get("level", "intermediate")

        is_correct = False

        if not student_ans:
            weak_areas.append(q["question"])

        elif q["type"] == "mcq":
            if _normalize_answer(student_ans) == _normalize_answer(correct):
                score += 1
                is_correct = True
            else:
                weak_areas.append(q["question"])

        else:  # short_answer
            if _normalize_answer(correct)[:30] in _normalize_answer(student_ans):
                score += 1
                is_correct = True
            else:
                weak_areas.append(q["question"])

        detailed_results.append({
            "question": q["question"],
            "your_answer": student_ans,
            "correct_answer": correct,
            "is_correct": is_correct,
            "level": level
        })

    return score, total, weak_areas, detailed_results


# =========================
# OPTIONAL LLM FEEDBACK FALLBACK
# =========================
def _llm_feedback(topic: str, weak_areas: List[str]) -> Dict[str, Any]:
    if not weak_areas:
        return {
            "feedback": "Excellent work! You have a strong understanding of the topic.",
            "suggestions": [
                "Try more advanced questions",
                "Explore deeper concepts",
                "Practice real-world applications"
            ]
        }

    prompt = f"""
You are an evaluator agent.

Topic: {topic}

Weak Areas:
{chr(10).join("- " + w for w in weak_areas)}

Generate:
1. Short feedback
2. 3 improvement suggestions

Return JSON:
{{
 "feedback": "...",
 "suggestions": ["...", "...", "..."]
}}
"""

    try:
        response = ollama.chat(
            model="qwen2.5:3b",
            messages=[{"role": "user", "content": prompt}],
        )

        raw = response["message"]["content"].strip()
        return json.loads(raw)

    except Exception:
        return {
            "feedback": "You need to revise weak areas.",
            "suggestions": [
                "Review key concepts",
                "Practice more questions",
                "Focus on weak topics"
            ]
        }


# =========================
# MAIN AGENT
# =========================
def evaluator_agent(state: Dict[str, Any]) -> Dict[str, Any]:
    logs = state.setdefault("logs", [])

    topic = state.get("topic", "")
    questions = state.get("quiz_questions", [])
    answers = state.get("student_answers", [])
    answer_key = state.get("answer_key", [])

    if not questions or not answer_key:
        raise ValueError("Missing quiz data for evaluation")

    if len(answers) != len(answer_key):
        answers = answers[:len(answer_key)]

    try:
        # =========================
        # STEP 1: GRADING
        # =========================
        score, total, weak_areas, detailed_results = _basic_grading(
            questions, answers, answer_key
        )

        percentage = round((score / total) * 100, 2) if total > 0 else 0

        # =========================
        # STEP 2: DIFFICULTY ANALYSIS
        # =========================
        difficulty_stats = {}

        for item in detailed_results:
            level = item["level"]
            difficulty_stats.setdefault(level, {"correct": 0, "total": 0})

            difficulty_stats[level]["total"] += 1
            if item["is_correct"]:
                difficulty_stats[level]["correct"] += 1

        # =========================
        # STEP 3: SMART FEEDBACK
        # =========================
        suggestions = _generate_smart_recommendations(
            score, total, weak_areas, difficulty_stats
        )

        if score == total:
            feedback = "Excellent performance! You mastered this topic."
        elif score >= total * 0.7:
            feedback = "Good job! You have a solid understanding."
        elif score >= total * 0.4:
            feedback = "Fair performance. There is room for improvement."
        else:
            feedback = "You need to improve your understanding of this topic."

        # =========================
        # STEP 4: FINAL RESULT
        # =========================
        result = {
            "score": score,
            "total": total,
            "percentage": percentage,
            "weak_areas": weak_areas,
            "detailed_results": detailed_results,
            "difficulty_stats": difficulty_stats,
            "feedback": feedback,
            "suggestions": suggestions
        }

        state["evaluation_result"] = result

        # =========================
        # LOGGING
        # =========================
        logs.append({
            "agent": "evaluator_agent",
            "status": "success",
            "score": score,
            "total": total,
            "percentage": percentage,
            "weak_areas_count": len(weak_areas)
        })

    except Exception as e:
        state["evaluation_result"] = {
            "score": 0,
            "total": len(answer_key),
            "percentage": 0,
            "feedback": "Evaluation failed",
            "suggestions": []
        }

        logs.append({
            "agent": "evaluator_agent",
            "status": "error",
            "error": str(e)
        })

    return state