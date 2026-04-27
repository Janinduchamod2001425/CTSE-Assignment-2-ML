from unittest.mock import Mock, patch

import pytest

from app.config import MAX_PLAN_STEPS
from tools.planning_tools import create_study_plan


def test_create_study_plan_returns_list():
    result = create_study_plan("Machine Learning", 30, "medium")

    assert isinstance(result, list)
    assert len(result) > 0


def test_create_study_plan_respects_max_size():
    result = create_study_plan("DBMS", 45, "hard")

    assert len(result) <= MAX_PLAN_STEPS


def test_create_study_plan_invalid_minutes():
    with pytest.raises(ValueError, match="minutes must be greater than 0"):
        create_study_plan("OOP", 0, "medium")


def test_create_study_plan_invalid_difficulty():
    with pytest.raises(ValueError, match="difficulty must be one of: easy, medium, hard"):
        create_study_plan("OOP", 20, "expert")


def test_create_study_plan_rejects_empty_topic():
    with pytest.raises(ValueError, match="topic must not be empty"):
        create_study_plan("", 20, "easy")


def test_create_study_plan_all_steps_are_strings():
    result = create_study_plan("Machine Learning", 30, "medium")

    assert all(isinstance(step, str) for step in result)


def test_create_study_plan_no_empty_steps():
    result = create_study_plan("Machine Learning", 30, "medium")

    assert all(step.strip() != "" for step in result)


def test_create_study_plan_structure_for_short_time():
    result = create_study_plan("CTSE", 10, "easy")

    assert isinstance(result, list)
    assert len(result) > 0
    assert len(result) <= MAX_PLAN_STEPS


def test_create_study_plan_parses_mocked_llm_output():
    mocked_response = Mock()
    mocked_response.content = (
        "1. Review the definition of Machine Learning\n"
        "2. Study supervised and unsupervised learning\n"
        "3. Understand common ML algorithms\n"
        "4. Practice simple ML examples\n"
        "5. Summarize key points"
    )

    with patch("tools.planning_tools.llm") as mocked_llm:
        mocked_llm.invoke.return_value = mocked_response
        result = create_study_plan("Machine Learning", 30, "medium")

    assert isinstance(result, list)
    assert len(result) >= 3
    assert len(result) <= MAX_PLAN_STEPS
    assert result[0] == "Review the definition of Machine Learning"


def test_create_study_plan_trims_numbering_from_mocked_output():
    mocked_response = Mock()
    mocked_response.content = (
        "1. Introduction to DBMS\n"
        "2. Core concepts of DBMS\n"
        "3. Practice DBMS examples"
    )

    with patch("tools.planning_tools.llm") as mocked_llm:
        mocked_llm.invoke.return_value = mocked_response
        result = create_study_plan("DBMS", 20, "easy")

    assert result[0] == "Introduction to DBMS"
    assert result[1] == "Core concepts of DBMS"
    assert result[2] == "Practice DBMS examples"


def test_create_study_plan_uses_fallback_when_llm_fails():
    with patch("tools.planning_tools.llm") as mocked_llm:
        mocked_llm.invoke.side_effect = Exception("LLM failure")
        result = create_study_plan("Machine Learning", 30, "medium")

    assert isinstance(result, list)
    assert len(result) > 0
    assert len(result) <= MAX_PLAN_STEPS


def test_create_study_plan_uses_fallback_for_weak_llm_output():
    mocked_response = Mock()
    mocked_response.content = "1. Too short"

    with patch("tools.planning_tools.llm") as mocked_llm:
        mocked_llm.invoke.return_value = mocked_response
        result = create_study_plan("Machine Learning", 30, "medium")

    assert isinstance(result, list)
    assert len(result) >= 3
    assert len(result) <= MAX_PLAN_STEPS