# Tóm tắt mô phỏng simulate-1@20261128-141756

Do `python run.py simulate` sinh ra — không sửa tay. Chép bảng sang `cost/cost-estimate.md`.

| Persona | Số phiên mô phỏng | Lượt hỏi / phiên | Token vào / phiên | Token ra / phiên | Gọi model / phiên | Gọi công cụ / phiên |
|---|---:|---:|---:|---:|---:|---:|
| dung_it | 26 | 1 | 480 | 54 | 0.7 | 2.2 |
| dung_vua | 15 | 2 | 990 | 113 | 1.3 | 4.6 |
| dung_nhieu | 9 | 3 | 1357 | 158 | 1.9 | 6.9 |

Tỉ lệ đạt dùng để tính: 19/24 (79%) — lượt run-2@20261128-084518

- Tỉ lệ đạt lấy từ lượt nhóm chọn: eval/run-2.csv (--rate-from).

| Model (giá) | Chi phí / phiên | Chi phí / task thành công | Chi phí / câu hỏi đạt | Chi phí / tháng — thấp (50 người) | Chi phí / tháng — cơ sở (107 người) | Chi phí / tháng — cao (147 người) | Chi phí / người / tháng (cơ sở) |
|---|---:|---:|---:|---:|---:|---:|---:|
| gemini-3.1-flash-lite (vào 0.25 · ra 1.5 $/1M) | $0.00033 | $0.00042 | $0.00025 | $0.0406 | $0.0868 | $0.1192 | $0.00081 |
| gemini-2.5-pro (vào 1.25 · ra 10.0 $/1M) | $0.0019 | $0.0024 | $0.0014 | $0.2304 | $0.4930 | $0.6772 | $0.0046 |

- Chi phí / task thành công = chi phí / phiên ÷ tỉ lệ đạt. Chi phí / câu hỏi đạt = chi phí / phiên ÷ số lượt hỏi trung bình mỗi phiên (1.7) ÷ tỉ lệ đạt — tỉ lệ đạt đo theo từng câu thử.
- Token đo trên model: gemini-3.1-flash-lite. Giá tính theo từng model trong bảng — model khác bộ tách token thì số token thật có thể lệch; ghi rõ "đo trên model X, tính giá model Y" trong cost/cost-estimate.md.
- Phiên lỗi (không tính vào trung bình): 0/50.
