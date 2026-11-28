# Khai báo dùng AI

README của nhóm có mục "Dùng AI vào việc gì" (2–3 dòng, bắt buộc). Ghi chi tiết vào bảng dưới đây.

> Luật của đề: dùng AI để làm bài thoải mái, nhưng **ai không giải thích được phần có tên mình thì phần đó nhận 0 điểm**. Khai thiếu không bị trừ; giấu mới bị.
> Ô `__ (tên tự điền)` là phần của thành viên đó, Minh không tự khai thay.

| Việc | Công cụ AI | AI làm gì | Người kiểm/sửa gì | Ai phụ trách |
|---|---|---|---|---|
| Code bản chạy thử | __ (Chuẩn tự điền) | __ | __ | Chuẩn |
| Prompt / thiết kế lời gọi mô hình | Claude Code (Minh) · __ (Chuẩn tự điền phần prompt trong `codebase/`) | Soạn nháp `spec.md` §4: sơ đồ, bảng công cụ, định dạng JSON AI phải trả, chỗ chặn rủi ro | Minh đọc, sửa và giải thích được từng nhánh trên sơ đồ | Minh (§4) · Chuẩn (prompt trong code) |
| Lời gọi mô hình trong sản phẩm | Gemini 3.1 Flash-Lite | Quyết định gợi ý / hỏi lại / từ chối, mỗi tin nhắn gọi 1 lần | Chặn lộ lời giải bằng code (`check_leak`), không nhờ AI tự kiểm | Chuẩn |
| Đào data (viết script đếm, gợi ý nhãn) | Claude Code (Minh, CP1) | Soạn bản đầu `evidence/count.py` và `evidence/data-mining.md` | Script có assert tự kiểm. Hùng kiểm tay __ dòng, khớp __ | Hùng |
| Rà câu hỏi phỏng vấn / khảo sát | Claude Code (Minh) | Soạn bộ câu hỏi và đoạn giới thiệu bối cảnh cho người được hỏi; chỉ rà câu dẫn dắt | Minh đọc lại trước khi hỏi P1 | Minh |
| Ghi chép phỏng vấn P1 | Claude Code (Minh) | Chép câu trả lời Minh ghi được vào khuôn `evidence/interviews/P1.md` | Trích dẫn là lời người được hỏi do Minh ghi rồi đưa cho AI; AI không thêm câu nào | Minh |
| Viết câu thử (benchmark) | __ (Huy tự điền) | __ | Mỗi câu thử có `source`; câu thử AI viết được ghi rõ | Huy |
| Sinh data `synthetic` (nếu có) | __ (Chuẩn / Hùng tự điền) | `data/labs.json`: 3 lab, 8 bước | Seed __ · kiểm tay __ dòng | Hùng |
| Chấm cột `pass` bằng LLM (nếu có) | Không dùng | — | Chấm tay toàn bộ. Huy và Hùng chấm độc lập 5 câu, khớp 5/5 (`eval/README.md` mục 3) | Huy, Hùng |
| Mô phỏng chi phí | Claude Code (Minh chạy hộ Hùng) | Chạy `python run.py simulate --rate-from eval/run-3.csv` (50 phiên, token đo bằng Gemini thật), viết lại `cost/cost-estimate.md`, điền `spec.md` §8 | Số trong bảng chép nguyên từ `cost/simulate-2-summary.md` do khung sinh ra. Hùng cần đọc lại và tự giải thích được | Hùng |
| Slide, văn bản | Claude Code (Minh) | Soạn nháp canvas, `spec.md` §0–§4 §6, `evidence/summary.md`, `docs/phan-cong.md`, slide `slides/demo-slides.html` → `demo-slides.pdf`, mục này | Minh đọc lại, đối chiếu từng số trên slide với file nguồn ghi ở chân trang. Chi phí trên slide 6 lấy từ `cost/simulate-2-summary.md` | Minh |
| Thử tay giải pháp tương tự (§3) | ChatGPT, CS50 Duck | Là đối tượng được thử, không phải công cụ làm bài | Minh dán nguyên văn câu trả lời vào `evidence/thu-tay-*.md` | Minh |

**Không dùng AI để:** tạo người được phỏng vấn, trích dẫn, câu trả lời khảo sát; sửa kết quả các lượt đã chạy (`eval/run-*.csv`, `cost/simulate-*.csv`, `traces/`).
