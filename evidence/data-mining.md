# Báo cáo phân tích hành vi mini lab pre-class

> Phương pháp và kết quả phân tích hành vi pre-class (05–25/11/2026). Chạy kiểm chứng: `python evidence/count.py` với dữ liệu BTC lưu nội bộ tại `data-btc/preclass/` (không commit dữ liệu gốc).

## 1. Nguồn dữ liệu và phương pháp thống kê

- **Data dùng:** `data-btc/preclass/` do BTC cấp (`events.csv`, `chat.csv`), dữ liệu từ 05/11/2026 đến 25/11/2026, đã ẩn danh.
- **Đếm gì:** kết cục của mỗi lần một học viên mở một mini lab.
  - Đơn vị đếm là **cặp (học viên `hv`, `lab_key`)**: mở lại nhiều lần vẫn tính là 1 cặp.
  - **Làm xong thật:** cặp có ≥1 sự kiện `lab_completed` với `skipped` khác `true`.
  - **Chỉ bấm bỏ qua:** cặp có `lab_completed` nhưng mọi lần đều `skipped = true`.
  - **Bỏ dở:** cặp có `lab_opened` mà không có `lab_completed` nào.
- **Mẫu số:** 538 cặp (học viên × lab) có `lab_opened`. Không dùng 721 tài khoản, cũng không dùng 436 học viên hoạt động, vì chỉ 147 người từng mở lab.
- **Để so hướng (bảng impact):** đếm lượt hỏi trợ giảng dưới video (`chat.csv` có `channel = video_question`).
  - Trường `moc_trich_dan` chỉ được ghi từ 13/11, nên mẫu số của tỉ lệ "không trích mốc giây" là 562 câu trả lời có ghi trường này, không phải 1.108.
- **Script:** [`evidence/count.py`](count.py). Có assert kiểm ba nhóm kết cục cộng lại đủ mẫu số. Đã chạy kiểm chứng ngày **27/11/2026**; các kết quả chính trong mục 3 khớp đầu ra script. Chỉ số riêng từ `answers.csv` và các phân tích theo lát thời gian không thuộc phạm vi kiểm chứng của lần chạy này.

## 2. Mẫu hành vi được ghi nhận

Đã đọc `event_types.csv`, `column_dictionary.csv` và ~50 dòng đầu của `events.csv`, `chat.csv`, `answers.csv`. Các *kiểu* hành vi thấy được:
- Mở lab rồi đóng tab, không có sự kiện kết thúc.
- Mở lab, khoảng 2 phút sau bấm "bỏ qua" khi chưa làm bước nào (`steps_done = 0`).
- Làm được 1 bước rồi bỏ qua bước cuối (`steps_done = 1`, `steps = 2`).
- Có trả lời bước thực hành (`answers.csv`, `nguon = thuc_hanh`), và tài liệu phân tích ban đầu ghi 496/519 câu đúng. **Chỉ số này chưa được tái kiểm chứng bằng `evidence/count.py`**; không dùng làm kết luận bổ sung khi chưa đối chiếu trực tiếp `answers.csv`.
- Theo các kênh ghi trong dữ liệu: `video_question`, `video_discussion_reply`, `session_question`; không có kênh chat được đánh dấu là gắn trực tiếp với lab. Chỉ số 145/436 trong script là số học viên có **bất kỳ bản ghi chat nào**, không phải số đã được xác minh hỏi AI.

## 3. Kết quả kiểm chứng

**Kết quả kiểm chứng ngày 27/11/2026:** 538 cặp đã mở; 344 hoàn thành, 98 chỉ bỏ qua và 96 bỏ dở; tổng không hoàn thành 194 (36,1%). Có 107/147 học viên đã mở lab từng không hoàn thành ít nhất một lab. Các tỷ lệ dưới đây tính theo mẫu số nêu rõ trong từng dòng.

| Đếm gì | x / N | % | Ghi chú |
|---|---|---|---|
| Cặp học viên × lab **không làm xong thật** | 194/538 | 36,1% | 98 chỉ bấm bỏ qua + 96 bỏ dở |
| · chỉ bấm bỏ qua | 98/538 | 18,2% | 59/98 lượt bỏ qua ngay ở bước 0, trung vị ~124 giây sau khi mở |
| · bỏ dở, không có sự kiện kết thúc | 96/538 | 17,8% | |
| Học viên có ≥1 lab không làm xong | 107/147 | 72,8% | Mẫu số: học viên từng mở ≥1 lab |
| Học viên từng mở ≥1 lab | 147/436 | 33,7% | Mẫu số: học viên có hoạt động |
| Lab `d01-lab-ban-la-llm`, không xong | 31/72 | 43,1% | Lab mở nhiều nhất |
| *(so hướng)* Học viên có bản ghi chat (mọi kênh) | 145/436 | 33,3% | Không thể suy ra toàn bộ đã hỏi AI; script hiện đếm mọi kênh trong `chat.csv` |
| *(so hướng)* Trả lời dưới video thiếu ngữ cảnh | 100/1.108 | 9,0% | `missing_context = true` |
| *(so hướng)* Trả lời không trích mốc giây | 231/562 | 41,1% | Phân tích trước đây ghi giảm từ ~54% xuống ~12% theo giai đoạn; chưa tái kiểm chứng bằng lần chạy này |

## 4. Ví dụ bản ghi đã mã hóa

Thời gian được ghi theo UTC (giờ Việt Nam = UTC + 7).
1. `L0578` · `d01-lab-xep-ban-context` (2 bước) · bấm bỏ qua ở bước 0/2, 70 giây sau khi mở · 09/11 15:13 UTC.
2. `L0094` · `d04-lab-thu-system-prompt` (1 bước) · bỏ qua ở bước 0/1, 141 giây sau khi mở · 10/11 05:36 UTC.
3. `L0287` · `d01-lab-ban-la-llm` · làm 1/2 bước rồi bỏ qua, 97 giây sau khi mở · 05/11 18:16 UTC (01:16 sáng giờ Việt Nam).
4. `L0665` · `d01-lab-ban-la-llm` · làm 1/2 bước rồi bỏ qua · 05/11 23:50 UTC.
5. `L0006` · `d01-lab-ban-la-llm` · mở lúc 05/11 10:56 UTC, không có sự kiện kết thúc nào.
6. `L0614` · `d01-lab-ban-la-llm` · mở lúc 05/11 17:17 UTC, không có sự kiện kết thúc nào.

## 5. Giới hạn phân tích và hướng kiểm chứng

- Data cho biết học viên **làm gì**, không cho biết **vì sao**. Bỏ qua ở bước 0 có thể là chưa thử (không có thời gian, nghĩ lab không bắt buộc), chứ chưa chắc là kẹt.
- "Bỏ dở" có thể là học viên làm lab ở chỗ khác (máy riêng, Colab) rồi không quay lại bấm xong.
- Data không có câu chữ học viên viết, nên không biết họ kẹt ở lỗi gì.
- Chỉ 147/436 học viên hoạt động từng mở lab. Tỉ lệ 36% là của người đã mở lab, **không phải của toàn khoá**.

**Kiểm chứng định tính:** nhóm thực hiện phỏng vấn tối thiểu 4 học viên ngoài nhóm (mỗi thành viên một người), tập trung vào lần gần nhất học viên không hoàn thành mini lab, bước đang thực hiện, cách xử lý và lý do dừng. Kết quả phỏng vấn chưa được sử dụng để kết luận nguyên nhân trong báo cáo này.
