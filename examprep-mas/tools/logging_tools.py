import json
import logging
import os
from typing import Dict, Any


LOG_DIR = "logs"
APP_LOG_FILE = os.path.join(LOG_DIR, "app.log")
TRACE_FILE = os.path.join(LOG_DIR, "execution_trace.jsonl")

os.makedirs(LOG_DIR, exist_ok=True)

logging.basicConfig(
    filename=APP_LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


def write_app_log(message: str) -> None:
    """Write a simple application log message."""
    logging.info(message)


def write_trace_log(data: Dict[str, Any]) -> None:
    """Append structured execution trace data to JSONL file."""
    with open(TRACE_FILE, "a", encoding="utf-8") as f:
        f.write(json.dumps(data, ensure_ascii=False) + "\n")