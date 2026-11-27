# Data card — dữ liệu bản chạy thử

## Dataset 1 · Bộ minh họa gợi ý mini lab về prompt

| Trường | Mô tả |
|---|---|
| Dùng để làm gì | Nguồn cho `search_lab_step` trong `codebase/tools.py`; cung cấp yêu cầu và gợi ý để agent thử luồng hỗ trợ từng bước. |
| Từ đâu | Nhóm/coding agent tự soạn; **synthetic**, không phải dữ liệu BTC, không phải bài lab chính thức và không phải dữ liệu Hùng viết. |
| Xử lý | Tự soạn thủ công 8 bước, lưu JSON; không lọc dữ liệu người học, không có dữ liệu cá nhân, không chia tập. |
| Số dòng / số đoạn | 8 bước trong `data/labs.json`. |
| Phiên bản / ngày lấy | `synthetic-prompt-lab-v1`, 27/11/2026; không có ngày lấy dữ liệu nguồn. |
| Nhãn | `synthetic`. |
| Giới hạn | Chỉ minh họa các khái niệm prompt/LLM; không phản ánh nội dung, lời giải, độ khó hoặc cách chấm của mini lab thật. Không dùng làm bằng chứng pain hay để tuyên bố chất lượng trên học viên. |

**Cách sinh / seed:** tự soạn thủ công theo lát cắt A6 trong `spec.md`; không dùng sinh ngẫu nhiên nên không có seed. Bộ dữ liệu khai rõ nguồn ngay trong từng bản ghi.

**Người kiểm theo phân công:** Phạm Lê Chuẩn. Rà soát nội dung trong phiên này do Codex (coding agent hỗ trợ phần bản chạy thử) thực hiện: 8/8 yêu cầu và gợi ý đều được đọc, gợi ý chỉ hướng thao tác tiếp theo và không ghi đáp án hoàn chỉnh. Việc rà này chỉ áp dụng cho bộ synthetic ở trên; chưa rà được dữ liệu Hùng viết vì dữ liệu đó không có trong workspace.

## Dataset 2

Chưa có. Không đưa dữ liệu cá nhân thật hoặc nguyên file data BTC cấp vào repo.
