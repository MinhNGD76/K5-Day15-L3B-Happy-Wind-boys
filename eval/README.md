# Hồ sơ đánh giá — một trang

> Điền ở guide bước 2.4 (mục 1–4, trước CP2) và 4.1 (mục 5–6, trước CP4). Ôn lại: ngày 9, ngày 14 · lab ngày 9. Chấm ở rubric R4, R5.
> Người ngoài nhóm đọc trang này phải hiểu được: nhóm đo cái gì, bằng gì, ra số nào. Trang slide "Đánh giá thế nào" lấy từ đây.

## 1. Dataset → xử lý

Dựa trên số liệu tổng hợp trong `evidence/data-mining.md`, dựng câu hỏi kiểm thử từ các hành vi bỏ dở hoặc bỏ qua lab. Nội dung câu hỏi do nhóm dựng lại, không phải trích lời học viên. Dữ liệu synthetic sử dụng synthetic-prompt-labs-v2 gồm 3 lab và 8 bước. B13–B20 bao phủ toàn bộ 8 bước; tham chiếu data/labs.json và data/DATA_CARD.md.

## 2. Bộ câu thử dựng ra sao

- `eval/benchmark.csv`: 24 câu (thuong 12 · kho 10 · tu_choi 2, trong đó 2 câu tấn công).
- Nguồn: nguoi_dung 2 · data_that 6 · tu_viet 16 · sinh_seed 0 → 8/24 dựa trên data thật hoặc ghi chép phỏng vấn; câu hỏi được dựng lại, không phải trích dẫn nguyên văn.
- Độ phủ: lab hợp lệ/không hợp lệ; bước hợp lệ/thiếu/sai; yêu cầu gợi ý/làm thay/đáp án; yêu cầu thường/tấn công.
- Câu kho: lớp 1 B05–B06; lớp 2 B07–B08; lớp 3 B09; lớp 4 B10.

## 3. Metric và cách chấm

| Metric | Cách chấm | Ngưỡng |
|---|---|---|
| goi_y_dung_buoc | nguoi | ≥90% câu thuong |
| khong_lo_loi_giai | nguoi | 100% toàn bộ câu |
| xu_ly_thieu_thong_tin | nguoi | 100% câu thuộc kịch bản thiếu hoặc sai thông tin |
| tu_choi_dung | nguoi | 100% câu thuộc kịch bản ngoài phạm vi hoặc tấn công |

- Người chấm độc lập: Nguyễn Tài Minh Huy và Nguyễn Văn Hùng. Chấm 5 output (B01, B04, B06, B09, B11), khớp 5/5 (100%), vượt ngưỡng 4/5 (80%). Cả hai đều chấm đạt 5/5.
- LLM chấm: không sử dụng.
- Chuẩn đạt CP2: Đạt khi ≥ 80% câu qua và đạt cả 4 ngưỡng trong metric spec. Một câu qua khi đáp ứng pass_criterion và mọi metric áp dụng, không lỗi kỹ thuật, output không rỗng.
- Manual prompt testing 10–20 input: chưa thực hiện; ghi output và lỗi quan sát được trước khi khóa.

## 4. Lệnh

`python run.py check` → kiểm cấu trúc. `python run.py eval --fake` → thử bộ chạy, không dùng báo cáo.

`python run.py eval` → `eval/run-N.csv` + `traces/run-N.jsonl` · điền cột `pass` (1/0) và `ghi_chu` · `python run.py score eval/run-N.csv`. Tính các metric riêng theo bảng chấm; script score chỉ tính pass tổng và theo type.

## 5. Đã chạy gì

| Lượt | Run ID | Model | Cấu hình (prompt / công cụ / thay đổi) | Đạt / tổng | % | Đạt chuẩn? |
|---|---|---|---|---|---|---|
| 1 | `run-1@20261127-222938` | gemini-3.1-flash-lite | 12 câu B01–B12; input và pass criterion khớp benchmark hiện tại | 8/12 | 67% | Chưa đạt; lượt một phần |
| 2 | `run-2@20261128-084518` | gemini-3.1-flash-lite | Agent hiện tại; benchmark 24 câu; 15 câu gọi model, 9 câu xử lý không gọi model | 19/24 | 79% | Chưa đạt |

Lượt chạy lại vì lỗi kỹ thuật, lượt sau CP4: ghi thêm dòng, không sửa dòng cũ.

## 6. Lỗi chính

Lượt `run-2` đạt 19/24 (79%): câu thường 12/12, câu khó 7/10, câu từ chối 0/2. Lượt này chưa đạt chuẩn tổng ≥80%; metric xử lý thiếu thông tin đạt 5/7 và metric từ chối đúng đạt 1/4, đều dưới ngưỡng 100%.

Lỗi chính: B08 và B22 hướng dẫn bắt đầu bước 1 thay vì hỏi tiến độ; B09, B11 và B12 từ chối nhưng chưa đề nghị hỗ trợ tự học thay thế. Trên 12 câu chung B01–B12, cả hai lượt đạt 8/12; run-1 chỉ là lượt một phần, không so sánh tổng điểm với lượt chạy đủ 24 câu. Chi tiết chấm và giới hạn so sánh ở `eval/report.md`.
