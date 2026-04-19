from agents.content_agent import content_agent
from tools.notes_tools import read_notes
import pytest
import json


def test_content_agent_generates_lesson_content():

    # 🔹 Load mock state from file
    with open("data/notes/sample_inputs/mock_state.json") as f:
        state = json.load(f)

    result = content_agent(state)

    assert "lesson_content" in result
    assert isinstance(result["lesson_content"], str)
    assert len(result["lesson_content"]) > 0
    assert len(result["logs"]) > 0


def test_read_notes_invalid_topic():
    with pytest.raises(FileNotFoundError):
        read_notes("Unknown Topic")