import json
from pathlib import Path


def load_json(file_path: str) -> dict:
    """Load a JSON file."""
    with Path(file_path).open(encoding="utf-8") as f:
        json.load(f)


def save_json(data: dict, file_path: str) -> None:
    """Save data to a JSON file."""
    with Path(file_path).open(encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def file_exists(file_path: str) -> bool:
    """Check if a file exists."""
    return Path(file_path).exists()
