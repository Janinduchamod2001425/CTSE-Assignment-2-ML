from typing import Any, Dict, List
import json
import random
import re
import ollama


def _extract_json_array(raw_text: str) -> List[Dict[str, Any]]:
    raw_text = raw_text.strip()

    try:
        data = json.loads(raw_text)
        if isinstance(data, list):
            return data
    except Exception:
        pass

    match = re.search(r"\[\s*{.*}\s*\]", raw_text, re.DOTALL)
    if match:
        try:
            data = json.loads(match.group(0))
            if isinstance(data, list):
                return data
        except Exception:
            pass

    raise ValueError("Could not parse quiz JSON from model output")


def _normalize_question(
    question: Dict[str, Any],
    idx: int,
    default_level: str
) -> Dict[str, Any]:
    q_type = str(question.get("type", "short_answer")).strip().lower()
    q_text = str(question.get("question", "")).strip()
    options = question.get("options", [])
    correct_answer = str(question.get("correct_answer", "")).strip()
    hint = str(question.get("hint", "")).strip()

    if q_type not in {"mcq", "short_answer"}:
        q_type = "short_answer"

    if q_type == "mcq":
        if not isinstance(options, list):
            options = []
        options = [str(opt).strip() for opt in options if str(opt).strip()]

        if len(options) < 4:
            q_type = "short_answer"
            options = []
        else:
            options = options[:4]
    else:
        options = []

    return {
        "id": idx,
        "type": q_type,
        "question": q_text,
        "options": options,
        "correct_answer": correct_answer,
        "hint": hint,
        "level": default_level,
    }


def _fallback_questions(
    topic: str,
    lesson_content: str,
    num_questions: int,
    quiz_level: str,
    question_type_mode: str
) -> List[Dict[str, Any]]:
    lines = [line.strip() for line in lesson_content.splitlines() if line.strip()]
    source_text = " ".join(lines) if lines else topic

    base_questions: List[Dict[str, Any]] = []

    for i in range(num_questions):
        make_mcq = (
            question_type_mode == "mcq" or
            (question_type_mode == "mixed" and i % 2 == 0)
        )

        if make_mcq:
            correct = f"A key concept in {topic}"
            options = [
                correct,
                "An unrelated cooking recipe",
                "A random sports strategy",
                "A music performance style",
            ]
            random.shuffle(options)

            base_questions.append({
                "id": i + 1,
                "type": "mcq",
                "question": f"Which option best relates to the topic '{topic}'?",
                "options": options,
                "correct_answer": correct,
                "hint": f"Think about the main concept in {topic}.",
                "level": quiz_level,
            })
        else:
            snippet = source_text[:120] + "..." if len(source_text) > 120 else source_text
            base_questions.append({
                "id": i + 1,
                "type": "short_answer",
                "question": f"Explain one important idea from the lesson on '{topic}'.",
                "options": [],
                "correct_answer": snippet,
                "hint": "Write a short explanation based on the lesson.",
                "level": quiz_level,
            })

    return base_questions


def quiz_agent(state: Dict[str, Any]) -> Dict[str, Any]:
    topic = state.get("topic", "").strip()
    lesson_content = state.get("lesson_content", "").strip()
    difficulty = state.get("difficulty", "medium").strip().lower()

    num_questions = state.get("num_quiz_questions", 5)
    quiz_level = state.get("quiz_level", "intermediate").strip().lower()
    quiz_style = state.get("quiz_style", "practice").strip().lower()
    question_type_mode = state.get("question_type_mode", "mixed").strip().lower()

    logs = state.setdefault("logs", [])

    if not topic:
        raise ValueError("Missing topic in state")

    if not lesson_content:
        raise ValueError("Lesson content is empty. Quiz cannot be generated.")

    if not isinstance(num_questions, int) or num_questions <= 0:
        num_questions = 5

    if num_questions > 25:
        num_questions = 25

    if quiz_level not in {"basic", "intermediate", "difficult"}:
        quiz_level = "intermediate"

    if quiz_style not in {"exam", "practice", "revision", "challenge"}:
        quiz_style = "practice"

    if question_type_mode not in {"mixed", "mcq", "short_answer"}:
        question_type_mode = "mixed"

    system_prompt = """
You are a quiz generator for an exam preparation multi-agent system.

Return ONLY valid JSON array.
Do not return markdown.
Do not return explanations outside JSON.

Each item must have:
- type: "mcq" or "short_answer"
- question: string
- options: array (4 options for mcq, [] for short_answer)
- correct_answer: string
- hint: string
"""

    user_prompt = f"""
Generate exactly {num_questions} quiz questions.

Topic: {topic}
Lesson Content:
{lesson_content}

Study Difficulty: {difficulty}
Quiz Level: {quiz_level}
Quiz Style: {quiz_style}
Question Type Mode: {question_type_mode}

Rules:
- If mode is "mcq", all questions must be mcq
- If mode is "short_answer", all questions must be short_answer
- If mode is "mixed", generate a balanced mix
- Keep all questions based only on the lesson content
- Make the quiz quality match the quiz style
- basic = easy recall
- intermediate = understanding and application
- difficult = deeper reasoning
- exam = more formal
- practice = balanced
- revision = quick memory-focused
- challenge = more tricky
"""

    try:
        response = ollama.chat(
            model="qwen2.5:3b",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
        )

        raw_output = response["message"]["content"].strip()
        parsed = _extract_json_array(raw_output)

        questions: List[Dict[str, Any]] = []
        for idx, item in enumerate(parsed[:num_questions], start=1):
            normalized = _normalize_question(item, idx, quiz_level)
            if normalized["question"]:
                questions.append(normalized)

        if len(questions) < num_questions:
            extra = _fallback_questions(
                topic=topic,
                lesson_content=lesson_content,
                num_questions=(num_questions - len(questions)),
                quiz_level=quiz_level,
                question_type_mode=question_type_mode,
            )
            for extra_item in extra:
                extra_item["id"] = len(questions) + 1
                questions.append(extra_item)

    except Exception as e:
        questions = _fallback_questions(
            topic=topic,
            lesson_content=lesson_content,
            num_questions=num_questions,
            quiz_level=quiz_level,
            question_type_mode=question_type_mode,
        )

        logs.append({
            "agent": "quiz_agent",
            "status": "fallback_used",
            "reason": str(e),
        })

    answer_key = []
    for q in questions:
        answer_key.append({
            "id": q["id"],
            "type": q["type"],
            "correct_answer": q["correct_answer"],
        })

    state["quiz_questions"] = questions
    state["answer_key"] = answer_key

    logs.append({
        "agent": "quiz_agent",
        "status": "success",
        "input": {
            "topic": topic,
            "num_questions": num_questions,
            "quiz_level": quiz_level,
            "quiz_style": quiz_style,
            "question_type_mode": question_type_mode,
        },
        "output_preview": [q["question"] for q in questions[:3]],
    })

    return state