"""Nối model — chỗ DUY NHẤT trong bản chạy thử gọi model AI. NHÓM VIẾT phần gọi model thật.

Hợp đồng (giữ nguyên để khung đo được token):
    call_model(system: str, user: str) -> dict với 4 khoá
        "text":       str   chữ model trả về
        "model":      str   tên model đã gọi (để tra giá ở bảng giá model)
        "tokens_in":  int   số token vào, lấy từ trường usage trong phản hồi API — KHÔNG ước lượng
        "tokens_out": int   số token ra, gồm cả token suy luận / suy nghĩ nếu API tính riêng
    @model_call (từ tracing.py) tự ghi mỗi lần gọi vào trace; agent.py gọi call_model bao nhiêu lần
    cũng được, khung tự cộng token.
    Lỗi gọi model (hết lượt, sai key, mất mạng): cứ để exception bay ra — khung ghi lỗi vào cột error.

Chế độ giả (mặc định khi .env chưa có MODEL_PROVIDER, hoặc MODEL_PROVIDER=fake):
    trả một câu giả cố định, model "fake", token 0 — để luồng chạy hết từ trước CP2 (guide bước 3.2).
    Lượt `run.py eval` / `run.py simulate` chạy bằng model giả KHÔNG được tính.

Nối model thật: điền .env (chép từ .env.example), rồi viết nhánh gọi API ở dưới theo docs/connect-model.md
(có ví dụ OpenAI, Claude, model chạy trên máy, và cách nối nhà cung cấp khác). Không dán API key vào file này.
"""
import json
import os
import socket
import time
import urllib.error
import urllib.parse
import urllib.request

from tracing import model_call

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

RETRYABLE_HTTP_STATUS = {429, 500, 502, 503, 504}
MAX_RETRIES = 3  # retries after the initial request; at most four HTTP attempts
MAX_RETRY_AFTER = 30.0


def load_env(path=os.path.join(ROOT, ".env")):
    """Đọc file .env (KEY=VALUE mỗi dòng) vào biến môi trường, không ghi đè biến đã có. Khung — không cần sửa."""
    if not os.path.exists(path):
        return
    with open(path, encoding="utf-8-sig") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, value = line.split("=", 1)
            os.environ.setdefault(key.strip(), value.strip().strip('"').strip("'"))


load_env()
MODEL_PROVIDER = (os.environ.get("MODEL_PROVIDER") or "fake").strip().lower()
MODEL_NAME = (os.environ.get("MODEL_NAME") or "").strip()
API_KEY = (os.environ.get("API_KEY") or "").strip()


def _post_json(url: str, headers: dict, body: dict, timeout: int = 25) -> dict:
    """POST JSON and return a decoded JSON response without exposing credentials."""
    request = urllib.request.Request(
        url,
        data=json.dumps(body, ensure_ascii=False).encode("utf-8"),
        headers={"Content-Type": "application/json", **headers},
        method="POST",
    )
    for attempt in range(MAX_RETRIES + 1):
        try:
            with urllib.request.urlopen(request, timeout=timeout) as response:
                payload = response.read().decode("utf-8")
            break
        except urllib.error.HTTPError as exc:
            raw_detail = exc.read().decode("utf-8", "replace")[:500]
            if attempt < MAX_RETRIES and exc.code in RETRYABLE_HTTP_STATUS:
                retry_after = exc.headers.get("Retry-After") if exc.headers else None
                try:
                    delay = min(max(float(retry_after), 0.0), MAX_RETRY_AFTER) if retry_after else 2 ** attempt
                except (TypeError, ValueError):
                    delay = 2 ** attempt
                time.sleep(delay)
                continue
            detail = raw_detail.replace(API_KEY, "[REDACTED]") if API_KEY else raw_detail
            raise RuntimeError("Gemini API HTTP %s: %s" % (exc.code, detail)) from None
        # socket.timeout: hết giờ lúc đang đọc phản hồi không bị gói thành URLError (= TimeoutError từ 3.10)
        except (urllib.error.URLError, socket.timeout) as exc:
            if attempt < MAX_RETRIES:
                time.sleep(2 ** attempt)
                continue
            raise RuntimeError("Không kết nối được Gemini API: %s" % getattr(exc, "reason", exc)) from None
    try:
        return json.loads(payload)
    except json.JSONDecodeError:
        raise RuntimeError("Gemini API trả về JSON không hợp lệ") from None


def _call_gemini(system: str, user: str) -> dict:
    if not API_KEY:
        raise RuntimeError("Thiếu API_KEY trong .env để gọi Gemini")
    if not MODEL_NAME:
        raise RuntimeError("Thiếu MODEL_NAME trong .env để gọi Gemini")

    model = urllib.parse.quote(MODEL_NAME, safe="")
    url = "https://generativelanguage.googleapis.com/v1beta/models/%s:generateContent" % model
    body = {
        "contents": [{"role": "user", "parts": [{"text": user}]}],
        "generationConfig": {"maxOutputTokens": 256, "temperature": 0},
    }
    if system:
        body["systemInstruction"] = {"parts": [{"text": system}]}

    data = _post_json(url, {"x-goog-api-key": API_KEY}, body)
    candidates = data.get("candidates") or []
    parts = (candidates[0].get("content") or {}).get("parts") or [] if candidates else []
    text = "".join(part.get("text", "") for part in parts if isinstance(part, dict))
    if not text.strip():
        feedback = data.get("promptFeedback") or {}
        reason = feedback.get("blockReason") or (candidates[0].get("finishReason") if candidates else "no candidate")
        raise RuntimeError("Gemini không trả văn bản (lý do: %s)" % reason)

    usage = data.get("usageMetadata") or {}
    if "promptTokenCount" not in usage or "candidatesTokenCount" not in usage:
        raise RuntimeError("Gemini response thiếu usageMetadata token cần thiết")
    tokens_in = int(usage["promptTokenCount"])
    tokens_out = int(usage["candidatesTokenCount"]) + int(usage.get("thoughtsTokenCount") or 0)
    return {"text": text, "model": MODEL_NAME, "tokens_in": tokens_in, "tokens_out": tokens_out}


@model_call
def call_model(system: str, user: str) -> dict:
    if MODEL_PROVIDER == "fake":
        last = (user.strip().splitlines() or [""])[-1]
        return {"text": "[câu trả lời giả — chưa nối model] " + last[:60], "model": "fake", "tokens_in": 0, "tokens_out": 0}

    if MODEL_PROVIDER == "gemini":
        return _call_gemini(system, user)

    # Add other real providers here when the project needs them.
    raise NotImplementedError(
        "chưa viết phần gọi model thật cho MODEL_PROVIDER=%s trong codebase/ai.py — xem docs/connect-model.md"
        % MODEL_PROVIDER)
