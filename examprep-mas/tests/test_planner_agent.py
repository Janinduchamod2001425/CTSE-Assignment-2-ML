from tools.planning_tools import create_study_plan


def test_create_study_plan_returns_list():
    result = create_study_plan("Machine Learning", 30, "medium")
    assert isinstance(result, list)
    assert len(result) > 0


def test_create_study_plan_short_time():
    result = create_study_plan("DBMS", 10, "easy")
    assert len(result) >= 1


def test_create_study_plan_invalid_minutes():
    try:
        create_study_plan("OOP", 0, "medium")
        assert False
    except ValueError:
        assert True