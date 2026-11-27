"""Read-only retrieval and solution-leak checks for synthetic lab content."""
import json
import os
import re
import unicodedata

from tracing import tool

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LABS_PATH = os.path.join(ROOT, "data", "labs.json")


def _normalize(text):
    decomposed = unicodedata.normalize("NFKD", str(text).casefold())
    plain = "".join(ch for ch in decomposed if not unicodedata.combining(ch))
    plain = plain.replace("đ", "d")
    return " ".join(re.findall(r"[\w]+", plain, flags=re.UNICODE))


def _load_labs():
    try:
        with open(LABS_PATH, encoding="utf-8") as source:
            data = json.load(source)
    except (OSError, ValueError) as exc:
        raise RuntimeError("Không đọc được data/labs.json: %s" % exc) from None
    labs = data.get("labs") if isinstance(data, dict) else None
    if not isinstance(labs, list):
        raise RuntimeError("data/labs.json cần có danh sách labs")
    return labs


@tool
def find_lab(message: str):
    """Tìm lab được nêu rõ trong tin nhắn.

    Input: tin nhắn học viên (str).
    Output: dict gồm lab_key, tên lab, số bước; hoặc dict rỗng nếu không tìm thấy.
    Tác động ngoài: không; chỉ đọc data/labs.json.
    """
    normalized = _normalize(message)
    if not normalized:
        return {}
    matches = []
    for lab in _load_labs():
        candidates = [lab.get("lab_key", "")] + lab.get("aliases", [])
        for candidate in candidates:
            term = _normalize(candidate)
            if term and re.search(r"(?<!\w)%s(?!\w)" % re.escape(term), normalized):
                matches.append(lab)
                break
    if len(matches) != 1:
        return {}
    lab = matches[0]
    return {
        "lab_key": lab["lab_key"],
        "name": lab["title"],
        "step_count": len(lab.get("steps", [])),
    }


@tool
def get_lab_step(lab_key: str):
    """Lấy đề, gợi ý và lỗi hay gặp mà model được phép xem.

    Input: mã lab (str).
    Output: dict lab_key, tên, số bước và bước đã lọc; không chứa lời giải hay leak_signals.
    Tác động ngoài: không; chỉ đọc data/labs.json.
    """
    for lab in _load_labs():
        if lab.get("lab_key") != lab_key:
            continue
        return {
            "lab_key": lab["lab_key"],
            "name": lab["title"],
            "step_count": len(lab.get("steps", [])),
            "steps": [
                {
                    "number": step["number"],
                    "task": step["task"],
                    "hint_level_1": step["hint_level_1"],
                    "hint_level_2": step["hint_level_2"],
                    "common_errors": step.get("common_errors", []),
                }
                for step in lab.get("steps", [])
            ],
        }
    return {}


@tool
def check_leak(text: str, lab_key: str) -> list:
    """So đầu ra với lời giải ẩn và tín hiệu lộ lời giải của lab.

    Input: chữ sắp gửi (str) và mã lab (str).
    Output: danh sách chuỗi mô tả dấu hiệu trùng; danh sách rỗng nghĩa là chưa phát hiện.
    Tác động ngoài: không; chỉ đọc data/labs.json.
    """
    output = _normalize(text)
    if not output:
        return []
    leaks = []
    for lab in _load_labs():
        if lab.get("lab_key") != lab_key:
            continue
        for step in lab.get("steps", []):
            solution = _normalize(step.get("solution", ""))
            if solution and solution in output:
                leaks.append("bước %d: trùng lời giải" % step["number"])
            for signal in step.get("leak_signals", []):
                normalized_signal = _normalize(signal)
                if normalized_signal and normalized_signal in output:
                    leaks.append("bước %d: trùng dấu hiệu lộ" % step["number"])
    return leaks
