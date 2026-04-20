#new one with better evaluation
from agents.content_agent import content_agent
import json
import os
import ollama
import pytest

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
MOCK_PATH = os.path.join(BASE_DIR, "data", "notes", "sample_inputs", "mock_state.json")


# =========================
# 1. RULE-BASED EVALUATION
# =========================
def evaluate_content(output: str) -> dict:
    score = 0

    # Structure checks
    if "# Topic:" in output:
        score += 1
    if "## 1." in output or "Section 1" in output:
        score += 1
    if "Summary" in output:
        score += 1

    # Content completeness
    if len(output.split()) > 80:
        score += 1

    return {
        "score": score,
        "passed": score >= 3
    }


def test_content_agent_evaluation():

    with open(MOCK_PATH) as f:
        state = json.load(f)

    result = content_agent(state)
    output = result["lesson_content"]

    evaluation = evaluate_content(output)

    assert evaluation["passed"] is True


# =========================
# 2. SECURITY VALIDATION
# =========================
def test_no_hallucination_keywords():

    forbidden_words = ["wikipedia", "google", "external source", "internet"]

    with open(MOCK_PATH) as f:
        state = json.load(f)

    result = content_agent(state)
    output = result["lesson_content"].lower()

    for word in forbidden_words:
        assert word not in output


# =========================
# 3. LLM-AS-A-JUDGE (ROBUST)
# =========================
def judge_output(output: str) -> str:
    try:
        response = ollama.chat(
            model="qwen2.5:3b",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a strict evaluator.\n"
                        "Check if the response:\n"
                        "1. Follows the required structure\n"
                        "2. Uses only given notes\n"
                        "3. Does not include external knowledge\n\n"
                        "Respond with ONLY one word: PASS or FAIL."
                    ),
                },
                {
                    "role": "user",
                    "content": output,
                },
            ],
        )

        return response["message"]["content"].strip().upper()

    except Exception:
        # Prevent test crash if Ollama not running
        pytest.skip("Ollama not available")


def test_llm_evaluation():

    with open(MOCK_PATH) as f:
        state = json.load(f)

    result = content_agent(state)
    output = result["lesson_content"]

    verdict = judge_output(output)

    # Ensure valid response
    assert verdict in ["PASS", "FAIL"]

    # Expect correct output
    assert verdict == "PASS"