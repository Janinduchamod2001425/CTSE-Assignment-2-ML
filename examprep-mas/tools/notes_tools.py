from pathlib import Path


def read_notes(topic: str, notes_dir: str = "data/notes") -> str:
    """
    Read local notes for a given topic.

    The topic name is mapped to a file in the notes directory.
    For example:
    - "Machine Learning" -> "ml.txt"
    - "OOP" -> "oop.txt"

    Args:
        topic: The topic requested by the user.
        notes_dir: The directory containing local notes files.

    Returns:
        The full text content of the matching notes file.

    Raises:
        FileNotFoundError: If no matching notes file exists.
        ValueError: If the file exists but is empty.
    """
    topic_map = {
        "machine learning": "ml.txt",
        "ml": "ml.txt",
        "oop": "oop.txt",
        "object oriented programming": "oop.txt",
        "iup": "iup.txt",
        "image understanding and processing": "iup.txt",
        "ctse": "ctse.txt",
    }

    normalized_topic = topic.strip().lower()
    filename = topic_map.get(normalized_topic)

    if not filename:
        raise FileNotFoundError(f"No mapped notes file found for topic: {topic}")

    file_path = Path(notes_dir) / filename

    if not file_path.exists():
        raise FileNotFoundError(f"Notes file does not exist: {file_path}")

    content = file_path.read_text(encoding="utf-8").strip()

    if not content:
        raise ValueError(f"Notes file is empty: {file_path}")

    return content