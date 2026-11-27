# Đào data — cách đếm và kết quả

> Điền ở guide bước 1.2. Script: [`evidence/count.py`](count.py). Chạy lại: đặt data BTC vào `data-btc/preclass/` (không commit) rồi `python evidence/count.py`.
> Repo chỉ chứa số đã tổng hợp và vài dòng ví dụ — không chép lại nguyên file data.

## 1. Cách đếm — viết TRƯỚC khi chạy

- **Data dùng:** `data/preclass/` do BTC cấp (`events.csv`, `chat.csv`), dữ liệu từ 05/11/2026 đến 25/11/2026, đã ẩn danh.
- **Đếm gì:** kết cục của mỗi lần một học viên mở một mini lab.
  - Đơn vị đếm là **cặp (học viên `hv`, `lab_key`)**: mở lại nhiều lần vẫn tính là 1 cặp.
  - **Làm xong thật:** cặp có ≥1 sự kiện `lab_completed` với `skipped` khác `true`.
  - **Chỉ bấm bỏ qua:** cặp có `lab_completed` nhưng mọi lần đều `skipped = true`.
  - **Bỏ dở:** cặp có `lab_opened` mà không có `lab_completed` nào.
- **Mẫu số:** 538 cặp (học viên × lab) có `lab_opened`. Không dùng 721 tài khoản, cũng không dùng 436 học viên hoạt động, vì chỉ 147 người từng mở lab.
- **Để so hướng (bảng impact):** đếm lượt hỏi trợ giảng dưới video (`chat.csv` có `channel = video_question`).
  - Trường `moc_trich_dan` chỉ được ghi từ 13/11, nên mẫu số của tỉ lệ "không trích mốc giây" là 562 câu trả lời có ghi trường này, không phải 1.108.
- **Script:** [`evidence/count.py`](count.py). Có assert kiểm ba nhóm kết cục cộng lại đủ mẫu số.

## 2. Đọc trước, đếm sau

Đã đọc `event_types.csv`, `column_dictionary.csv` và ~50 dòng đầu của `events.csv`, `chat.csv`, `answers.csv`. Các *kiểu* hành vi thấy được:
- Mở lab rồi đóng tab, không có sự kiện kết thúc.
- Mở lab, khoảng 2 phút sau bấm "bỏ qua" khi chưa làm bước nào (`steps_done = 0`).
- Làm được 1 bước rồi bỏ qua bước cuối (`steps_done = 1`, `steps = 2`).
- Có trả lời bước thực hành (`answers.csv`, `nguon = thuc_hanh`), và gần như luôn đúng (496/519). Nghĩa là ai đã nộp thì thường đúng, còn chỗ mất là ở những người không nộp.
- Không có kênh chat nào gắn với lab: `chat_sent` chỉ có `video_question`, `video_discussion_reply`, `session_question`. Học viên không hỏi AI được trong lúc làm lab.

## 3. Kết quả

| Đếm gì | x / N | % | Ghi chú |
|---|---|---|---|
| Cặp học viên × lab **không làm xong thật** | 194/538 | 36,1% | 98 chỉ bấm bỏ qua + 96 bỏ dở |
| · chỉ bấm bỏ qua | 98/538 | 18,2% | 59/98 lượt bỏ qua ngay ở bước 0, trung vị ~124 giây sau khi mở |
| · bỏ dở, không có sự kiện kết thúc | 96/538 | 17,8% | |
| Học viên có ≥1 lab không làm xong | 107/147 | 72,8% | Mẫu số: học viên từng mở ≥1 lab |
| Học viên từng mở ≥1 lab | 147/436 | 33,7% | Mẫu số: học viên có hoạt động |
| Lab `d01-lab-ban-la-llm`, không xong | 31/72 | 43,1% | Lab mở nhiều nhất |
| *(so hướng)* Học viên có hỏi trợ giảng AI | 145/436 | 33,3% | |
| *(so hướng)* Trả lời dưới video thiếu ngữ cảnh | 100/1.108 | 9,0% | `missing_context = true` |
| *(so hướng)* Trả lời không trích mốc giây | 231/562 | 41,1% | Giảm từ ~54% (13–17/11) xuống ~12% (18–25/11): trợ giảng đã tự cải thiện |

## 4. ≥5 ví dụ cụ thể (mã đã ẩn danh, không đoán ai là ai)

Giờ ghi theo UTC (giờ Việt Nam = UTC + 7).
1. `L0578` · `d01-lab-xep-ban-context` (2 bước) · bấm bỏ qua ở bước 0/2, 70 giây sau khi mở · 09/11 15:13 UTC.
2. `L0094` · `d04-lab-thu-system-prompt` (1 bước) · bỏ qua ở bước 0/1, 141 giây sau khi mở · 10/11 05:36 UTC.
3. `L0287` · `d01-lab-ban-la-llm` · làm 1/2 bước rồi bỏ qua, 97 giây sau khi mở · 05/11 18:16 UTC (01:16 sáng giờ Việt Nam).
4. `L0665` · `d01-lab-ban-la-llm` · làm 1/2 bước rồi bỏ qua · 05/11 23:50 UTC.
5. `L0006` · `d01-lab-ban-la-llm` · mở lúc 05/11 10:56 UTC, không có sự kiện kết thúc nào.
6. `L0614` · `d01-lab-ban-la-llm` · mở lúc 05/11 17:17 UTC, không có sự kiện kết thúc nào.

## 5. Giới hạn của data

- Data cho biết học viên **làm gì**, không cho biết **vì sao**. Bỏ qua ở bước 0 có thể là chưa thử (không có thời gian, nghĩ lab không bắt buộc), chứ chưa chắc là kẹt.
- "Bỏ dở" có thể là học viên làm lab ở chỗ khác (máy riêng, Colab) rồi không quay lại bấm xong.
- Data không có câu chữ học viên viết, nên không biết họ kẹt ở lỗi gì.
- Chỉ 147/436 học viên hoạt động từng mở lab. Tỉ lệ 36% là của người đã mở lab, **không phải của toàn khoá**.

→ **Kiểm lại bằng:** phỏng vấn ≥4 học viên ngoài nhóm (mỗi thành viên 1 người), hỏi: *"Lần gần nhất bạn mở một mini lab trên pre-class mà không làm xong là khi nào? Lúc đó bạn đang ở bước nào, đã làm gì, vì sao dừng?"*
