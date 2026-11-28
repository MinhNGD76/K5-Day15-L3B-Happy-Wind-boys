# Reflection — Phạm Lê Chuẩn (2A202603784)

1. Vai trò + phần mình làm (trỏ tới file / commit):
   Theo phân công, mình phụ trách bản chạy thử, nối Gemini và chặn rủi ro trong `codebase/`.
   Ở CP4, phần code liên quan gồm luồng từ chối/hỏi tiến độ trong `codebase/agent.py` và regression tests trong `codebase/test_safety.py` (commit `fd87442`).
   Phần hoàn thiện demo web và xử lý timeout hiện nằm ở `codebase/app.py`, `codebase/ai.py`.

2. AI hỗ trợ mình thế nào (việc gì, công cụ gì, chỗ nào phải sửa lại output AI):
   Mình dùng Codex để hỗ trợ chỉnh luồng agent, giao diện demo và cách xử lý lỗi gọi Gemini.
   Mình phải đối chiếu câu trả lời với đề synthetic trong `data/labs.json`, guardrails, benchmark và log thực tế; giao diện cũng cần bỏ nhãn, dòng căn cứ và disclaimer khỏi phần phản hồi.
   Khi API chậm, mình dùng log và trace để phân biệt câu hỏi được code xử lý trực tiếp với câu thực sự gọi Gemini.

3. Một câu thử trượt của nhóm và mình học được gì từ nó:
   B01 ở `run-3` bị `TimeoutError` khi gọi Gemini nên không có output hợp lệ, dù lần chạy sau ở `run-4` trả lời được.
   Mình học được rằng phải xem cả lỗi kỹ thuật và độ trễ, không chỉ chấm nội dung câu trả lời; timeout 60 giây cũng có thể quá ngắn khi model phản hồi chậm.
   `run-4` chưa được chấm theo rubric, nên cần giữ kết luận đó ở trạng thái chờ xác nhận.
