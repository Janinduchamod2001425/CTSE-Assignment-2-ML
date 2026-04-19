from agents.content_agent import content_agent
import json
import os
import ollama

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
MOCK_PATH = os.path.join(BASE_DIR, "data", "sample_inputs", "mock_state.json")


def evaluate_content(output: str) -> dict:
    score = 0

    if "# Topic:" in output:
        score += 1
    if "Summary" in output:
        score += 1
    if len(output) > 100:
        score += 1

    return {
        "score": score,
        "passed": score >= 2
    }


def test_content_agent_evaluation():

    with open(MOCK_PATH) as f:
        state = json.load(f)

    result = content_agent(state)
    output = result["lesson_content"]

    evaluation = evaluate_content(output)

    assert evaluation["passed"] is True

def test_no_hallucination_keywords():

    forbidden_words = ["Wikipedia", "Google", "external source"]

    with open(MOCK_PATH) as f:
        state = json.load(f)

    result = content_agent(state)
    output = result["lesson_content"]

    for word in forbidden_words:
        assert word not in output

def judge_output(output: str):

    response = ollama.chat(
        model="qwen2.5:3b",
        messages=[
            {
                "role": "system",
                "content": "You are an evaluator. Check if the answer follows instructions and is based only on given notes. Respond with PASS or FAIL."
            },
            {
                "role": "user",
                "content": output
            }
        ]
    )

    return response["message"]["content"]


def test_llm_evaluation():

    with open(MOCK_PATH) as f:
        state = json.load(f)

    result = content_agent(state)
    output = result["lesson_content"]

    verdict = judge_output(output)

    assert "PASS" in verdict