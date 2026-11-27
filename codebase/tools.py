"""Read-only lookup of the prototype lab's practice prompts and hints."""
import json
import os
import re

from tracing import tool

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LABS_PATH = os.path.join(ROOT, "data", "labs.json")


def _tokens(text):
    return set(re.findall(r"[\w-]+", str(text).lower(), flags=re.UNICODE))


@tool
def search_lab_step(query: str) -> list:
    """Tra gợi ý cho bước mini lab từ dữ liệu mẫu.

    Input: mô tả chỗ kẹt hoặc mã bước (str).
    Output: tối đa 3 đoạn gồm mã, yêu cầu, gợi ý và nguồn; không trả đáp án.
    Tác động ngoài: không; chỉ đọc data/labs.json.
    """
    if not isinstance(query, str) or not query.strip():
        return []

    try:
        with open(LABS_PATH, encoding="utf-8") as f:
            data = json.load(f)
    except (OSError, ValueError) as exc:
        raise RuntimeError("Không đọc được dữ liệu lab mẫu: %s" % exc)

    query_tokens = _tokens(query)
    # Explicit step numbers take priority (e.g. "bước 3").
    step_numbers = set(re.findall(r"(?:bước|step)\s*(\d+)", query.lower()))
    if not step_numbers:
        # Still identify an explicitly numbered step if a console mangles accents.
        step_numbers = set(re.findall(r"\d+", query))
    ranked = []
    for item in data.get("steps", []):
        searchable = " ".join((item.get("code", ""), item.get("title", ""), item.get("task", "")))
        words = _tokens(searchable)
        score = len(query_tokens & words)
        if step_numbers and str(item.get("step")) in step_numbers:
            score += 10
        if score:
            ranked.append((score, item))

    ranked.sort(key=lambda pair: (-pair[0], pair[1].get("step", 0)))
    return [
        {
            "code": item["code"],
            "title": item["title"],
            "task": item["task"],
            "hint": item["hint"],
            "source": item.get("source", ""),
        }
        for _, item in ranked[:3]
    ]
