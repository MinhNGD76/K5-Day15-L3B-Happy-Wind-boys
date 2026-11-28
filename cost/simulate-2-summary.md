# Tóm tắt mô phỏng simulate-2@20261128-143612

Do `python run.py simulate` sinh ra — không sửa tay. Chép bảng sang `cost/cost-estimate.md`.

| Persona | Số phiên mô phỏng | Lượt hỏi / phiên | Token vào / phiên | Token ra / phiên | Gọi model / phiên | Gọi công cụ / phiên |
|---|---:|---:|---:|---:|---:|---:|
| dung_it | 23 | 1 | 417 | 45 | 0.6 | 2.1 |
| dung_vua | 14 | 2 | 860 | 98 | 1.1 | 4.4 |
| dung_nhieu | 9 | 3 | 1205 | 138 | 1.7 | 6.7 |

Tỉ lệ đạt dùng để tính: 23/24 (96%) — lượt run-3@20261128-141616

- Tỉ lệ đạt lấy từ lượt nhóm chọn: eval/run-3.csv (--rate-from).

| Model (giá) | Chi phí / phiên | Chi phí / task thành công | Chi phí / câu hỏi đạt | Chi phí / tháng — thấp (50 người) | Chi phí / tháng — cơ sở (107 người) | Chi phí / tháng — cao (147 người) | Chi phí / người / tháng (cơ sở) |
|---|---:|---:|---:|---:|---:|---:|---:|
| gemini-3.1-flash-lite (vào 0.25 · ra 1.5 $/1M) | $0.00030 | $0.00031 | $0.00018 | $0.0355 | $0.0760 | $0.1044 | $0.00071 |
| gemini-2.5-pro (vào 1.25 · ra 10.0 $/1M) | $0.0017 | $0.0017 | $0.0010 | $0.2016 | $0.4314 | $0.5927 | $0.0040 |

- Chi phí / task thành công = chi phí / phiên ÷ tỉ lệ đạt. Chi phí / câu hỏi đạt = chi phí / phiên ÷ số lượt hỏi trung bình mỗi phiên (1.7) ÷ tỉ lệ đạt — tỉ lệ đạt đo theo từng câu thử.
- Token đo trên model: gemini-3.1-flash-lite. Giá tính theo từng model trong bảng — model khác bộ tách token thì số token thật có thể lệch; ghi rõ "đo trên model X, tính giá model Y" trong cost/cost-estimate.md.
- Phiên lỗi (không tính vào trung bình): 4/50.
