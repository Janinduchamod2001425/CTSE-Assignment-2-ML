from tools.planning_tools import create_study_plan


def test_create_study_plan_returns_list():
    result = create_study_plan("Machine Learning", 30, "medium")
    assert isinstance(result, list)
    assert len(result) > 0


def test_create_study_plan_respects_max_size():
    result = create_study_plan("DBMS", 45, "hard")
    assert len(result) <= 5


def test_create_study_plan_invalid_minutes():
    try:
        create_study_plan("OOP", 0, "medium")
        assert False
    except ValueError:
        assert True


def test_create_study_plan_invalid_difficulty():
    try:
        create_study_plan("OOP", 20, "expert")
        assert False
    except ValueError:
        assert True