from agents.content_agent import content_agent
from tools.notes_tools import read_notes
import pytest
import json
import os


BASE_DIR = os.path.dirname(os.path.dirname(__file__))
MOCK_PATH = os.path.join(BASE_DIR, "data", "notes", "sample_inputs", "mock_state.json")


# =========================
# 1. BASIC FUNCTIONAL TEST
# =========================
def test_content_agent_generates_lesson_content():

    with open(MOCK_PATH) as f:
        state = json.load(f)

    result = content_agent(state)

    assert "lesson_content" in result
    assert isinstance(result["lesson_content"], str)
    assert len(result["lesson_content"]) > 0
    assert len(result["logs"]) > 0


# =========================
# 2. STRUCTURE VALIDATION
# =========================
def test_output_structure():

    with open(MOCK_PATH) as f:
        state = json.load(f)

    result = content_agent(state)
    content = result["lesson_content"]

    assert "# Topic:" in content
    assert "## 1." in content or "Section 1" in content
    assert "Summary" in content


# =========================
# 3. DIFFICULTY TESTING
# =========================
def test_difficulty_easy_vs_hard():

    with open(MOCK_PATH) as f:
        base_state = json.load(f)

    easy_state = base_state.copy()
    easy_state["difficulty"] = "easy"

    hard_state = base_state.copy()
    hard_state["difficulty"] = "hard"

    easy_result = content_agent(easy_state)
    hard_result = content_agent(hard_state)

    # Ensure outputs exist
    assert len(easy_result["lesson_content"]) > 0
    assert len(hard_result["lesson_content"]) > 0

    # Optional heuristic check (length difference)
    assert easy_result["lesson_content"] != hard_result["lesson_content"]


# =========================
# 4. TIME CONSTRAINT TEST
# =========================
def test_time_constraint_behavior():

    with open(MOCK_PATH) as f:
        state = json.load(f)

    short_time_state = state.copy()
    short_time_state["time_minutes"] = 10

    long_time_state = state.copy()
    long_time_state["time_minutes"] = 60

    short_output = content_agent(short_time_state)["lesson_content"]
    long_output = content_agent(long_time_state)["lesson_content"]

    assert len(short_output) > 0
    assert len(long_output) > 0

    # Longer time should generally produce more content
    assert len(long_output) >= len(short_output)


# =========================
# 5. ERROR HANDLING TEST
# =========================
def test_read_notes_invalid_topic():
    with pytest.raises(FileNotFoundError):
        read_notes("Unknown Topic")


# =========================
# 6. EMPTY STUDY PLAN TEST
# =========================
def test_empty_study_plan():

    with open(MOCK_PATH) as f:
        state = json.load(f)

    state["study_plan"] = []

    result = content_agent(state)

    # Should not crash
    assert "lesson_content" in result
    assert isinstance(result["lesson_content"], str)


# =========================
# 7. LOGGING VALIDATION
# =========================
def test_logging_fields():

    with open(MOCK_PATH) as f:
        state = json.load(f)

    result = content_agent(state)

    logs = result["logs"]
    assert len(logs) > 0

    log_entry = logs[-1]

    assert "agent" in log_entry
    assert "status" in log_entry
    assert "topic" in log_entry