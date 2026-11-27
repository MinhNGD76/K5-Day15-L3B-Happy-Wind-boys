# Canvas — HappyWindBoys · Track A

> CP1 17:00 Thứ Sáu 27/11: bản đầu, đủ 7 dòng. CP2 19:30: cập nhật số bằng chứng, lát cắt đã chốt, dòng "Đã đổi gì so với CP1".

| # | Dòng | Nhóm điền |
|---|---|---|
| 1 | Track + lát cắt dự kiến | **Track A · EdTech.** Hỗ trợ mini lab pre-class: gợi ý bước tiếp theo cho học viên đang kẹt, không đưa lời giải |
| 2 | Người dùng chính (một vai cụ thể — không phải "học viên nói chung") | Học viên L3 AI20K K5 đi làm ban ngày, tối tự làm mini lab pre-class trước buổi học, không có lab coach bên cạnh |
| 3 | Pain một câu: ai — đang làm gì — vướng đâu — hậu quả | Học viên L3 tự làm mini lab trước buổi học bị kẹt ở một bước mà không có ai để hỏi ngay, nên bỏ dở hoặc bấm bỏ qua. Đến buổi lab trên lớp, họ thiếu phần thực hành nền |
| 4 | Bằng chứng đầu — CP1: giả thuyết + nguồn sẽ kiểm | **Số đầu từ data pre-class:** 194/538 (36,1%) lượt học viên × lab đã mở mà không làm xong thật. 107/147 (72,8%) học viên từng mở lab có ≥1 lab bỏ dở. Cách đếm: `evidence/data-mining.md`, `evidence/count.py`. **Giả thuyết:** bỏ vì kẹt, không phải vì thiếu giờ. **Sẽ kiểm:** phỏng vấn ≥4 học viên ngoài nhóm (`evidence/interviews/`) |
| 4b | *(CP2)* Số đầu tiên + 1 trích dẫn | **Số:** 194/538 (36,1%) lượt mở lab không xong. Trong đó 59/98 lượt bấm bỏ qua ngay ở bước 0, trung vị ~124 giây sau khi mở, nên chưa chắc là kẹt. **Ví dụ từ data:** `L0287` làm 1/2 bước lab `d01-lab-ban-la-llm` rồi bấm bỏ qua lúc 01:16 sáng giờ VN. **Trích dẫn người dùng:** *chưa có — đang phỏng vấn (`evidence/interviews/`)* |
| 5 | **Lát cắt MỘT CÂU** (1 người dùng · 1 việc · 1 quyết định AI · 1 kết quả) | *(chốt CP2)* Một học viên L3 · đang kẹt ở một bước mini lab pre-class, dán lỗi hoặc mô tả chỗ kẹt · AI quyết định đưa **một gợi ý bước tiếp theo** dựa trên đề lab (không đưa lời giải), hoặc hỏi lại khi thiếu thông tin, hoặc từ chối khi ngoài phạm vi · học viên tự làm qua được bước đó |
| 6 | AI tự làm đến đâu + 1 dòng lý do: sai thì ai chịu gì | **AI tự làm khi chắc, chuyển người khi không.** Gợi ý sai thì học viên mất vài phút và tự thấy được. Lộ lời giải thì mất giá trị học, nên chặn bằng một bước kiểm. Ngoài đề lab hoặc không chắc thì nói rõ và gợi ý hỏi lab coach |
| 7 | Phân công có tên | **Nguyễn Đình Minh (đội trưởng):** canvas, spec §1–2 §4, evidence/summary, slide, nộp CP · **Phạm Lê Chuẩn:** codebase, nối model, chặn rủi ro · **Nguyễn Tài Minh Huy:** benchmark, metric, spec §5 §7, eval/report · **Nguyễn Văn Hùng:** đào data, DATA_CARD, cost · **Cả nhóm:** mỗi người phỏng vấn ≥1 học viên |
| — | *(CP2)* Đã đổi gì so với CP1 | (1) Lát cắt thêm nhánh **từ chối** (hỏi điểm số, xin làm hộ, xin lời giải) bên cạnh gợi ý và hỏi lại. (2) Chặn lộ lời giải bằng code, không chỉ dặn trong prompt: lời giải không bao giờ vào prompt, và output được kiểm trước khi gửi. (3) Người dùng và pain giữ nguyên, chờ kết quả phỏng vấn |
