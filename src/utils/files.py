import json
from pathlib import Path

OUT = Path(__file__).resolve().parents[1].joinpath("outputs")
OUT.mkdir(parents=True, exist_ok=True)


def save_text(name: str, text: str):
    path = OUT.joinpath(name)
    path.write_text(text, encoding="utf-8")
    return str(path)


def save_json(name: str, obj):
    path = OUT.joinpath(name)
    path.write_text(json.dumps(obj, indent=2), encoding="utf-8")
    return str(path)
