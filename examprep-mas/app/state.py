from typing import TypedDict, List, Dict, Any


class ExamPrepState(TypedDict):
    user_request: str
    topic: str
    time_minutes: int
    difficulty: str
    notes_file_path: str

    study_plan: List[str]
    lesson_content: str
    quiz_questions: List[Dict[str, Any]]
    answer_key: List[Dict[str, Any]]
    student_answers: List[str]
    evaluation_result: Dict[str, Any]
    logs: List[Dict[str, Any]]