# Tổng hợp bằng chứng pain

> Chấm ở rubric R1. Người viết: Minh. Cập nhật 28/11/2026.
> Ô `__` hoặc *(chờ P_)* = chưa có, điền sau khi phỏng vấn xong. Không điền số chưa nghe được.

## 1. Nguồn đã dùng

| Nguồn | Đạt ngưỡng? | File |
|---|---|---|
| Đào data (x/N, %, cách đếm chạy lại được, ≥5 ví dụ) | ☑ 194/538, script `evidence/count.py` có assert, 6 ví dụ ở mục 4 | `evidence/data-mining.md` |
| Phỏng vấn (≥3 người ngoài nhóm, đúng người dùng) | ☑ 3/3 (P1, P3, P4) | `evidence/interviews/P1.md`… `P4.md` |
| Khảo sát (≥20 người ngoài nhóm, đúng người dùng) | ☐ không làm | — |

## 2. Số chính

- **Đào data:** 194/538 (36,1%) lượt mở mini lab (học viên × lab) không làm xong thật, gồm 98 lượt chỉ bấm bỏ qua và 96 lượt bỏ dở. 107/147 (72,8%) học viên từng mở lab có ít nhất 1 lab không xong. 59/98 lượt bỏ qua xảy ra ngay ở bước 0, trung vị ~124 giây sau khi mở. Lab mở nhiều nhất `d01-lab-ban-la-llm`: 31/72 (43,1%) không xong. Nguồn: `evidence/data-mining.md` mục 3, dữ liệu 05–25/11/2026.
- **Phỏng vấn:** 0/3 người nói kẹt là lý do chính để bỏ (P1 nói hết thời gian, P4 nói lỗi môi trường, P3 nói lab ngày càng khó và không đủ thời gian), nhưng cả 3 đều có kẹt ở một chỗ và đã tự xoay xở *(n nhỏ, không ghi %)* · số lần / tháng: P1 1, P2 __, P3 chưa có số / tháng (tự báo 2–3 lần / tuần với lab dài và khó), P4 ~1 · mỗi lần mất 20–60 phút (P1 ~20, P3 ~25–30, P4 ~60).

| | Vai | Gặp pain? | Số lần / 1 tháng qua | Lần gần nhất mất | Đang xoay xở bằng |
|---|---|---|---|---|---|
| P1 | Học viên ngoài nhóm (phỏng vấn trực tiếp) | Một phần: kẹt ở phần thảo luận nhóm của mini lab số 2 ngày thứ 2 (vẽ sơ đồ quy trình hiện tại), dừng vì hết thời gian | 1 | ~20 phút | Tìm trên mạng, dùng AI |
| P3 | Học viên L3 (phỏng vấn qua tin nhắn) | Một phần: lab Day 14, khó đọc và hiểu cấu trúc các file trong thư mục dự án. Chưa xác nhận đó là mini lab pre-class, cũng chưa xác nhận có bỏ lab hay không | Chưa có số / tháng; tự báo 2–3 lần / tuần với lab dài và khó | ~25–30 phút | Dùng AI tóm tắt yêu cầu và định hướng cách làm |
| P4 | Học viên ngoài nhóm | Một phần: bỏ lab ngày 14 vì không cài được Docker, rồi lỗi server trên Codespaces/Render | ~1 | ~60 phút | Tự thử môi trường khác (GitHub Codespaces, Render) |

## 3. ≥5 trích dẫn hoặc ví dụ nguyên văn (có nguồn, bỏ tên)

1. "tôi muốn gợi ý, vì từ đó có thể tự tìm ra đáp án" (P4, `evidence/interviews/P4.md`)
2. `L0578` · `d01-lab-xep-ban-context` (2 bước) · bấm bỏ qua ở bước 0/2, 70 giây sau khi mở · 09/11 15:13 UTC (`events.csv`, `data-mining.md` mục 4 ví dụ 1)
3. `L0094` · `d04-lab-thu-system-prompt` (1 bước) · bỏ qua ở bước 0/1, 141 giây sau khi mở · 10/11 05:36 UTC (`data-mining.md` mục 4 ví dụ 2)
4. `L0287` · `d01-lab-ban-la-llm` · làm 1/2 bước rồi bỏ qua, 97 giây sau khi mở · 01:16 sáng giờ Việt Nam (`data-mining.md` mục 4 ví dụ 3)
5. `L0665` · `d01-lab-ban-la-llm` · làm 1/2 bước rồi bỏ qua · 05/11 23:50 UTC (`data-mining.md` mục 4 ví dụ 4)
6. `L0006` · `d01-lab-ban-la-llm` · mở lúc 05/11 10:56 UTC, không có sự kiện kết thúc (`data-mining.md` mục 4 ví dụ 5)
7. "Gợi ý trước rồi đến đáp án. Vì hỏi luôn câu trả lời thì nghĩ làm gì và thông qua gợi ý thì mình cũng hiểu được thought process." (P1, `evidence/interviews/P1.md`)
   - Câu P1 kẹt, nguyên văn: "Sơ đồ trực quan hóa quy trình vận hành hiện tại. … Yêu cầu: Thể hiện rõ các bước tuần tự, điểm chuyển giao (🔄 Handoff), thời gian xử lý và điểm nghẽn cổ chai (🔴 Bottleneck)." (P1)
8. "Mình dùng AI để tóm tắt yêu cầu bài lab và định hướng cách làm" (P3, `evidence/interviews/P3.md`)
9. "Một phần lab càng ngày càng khó và thời gian cũng chưa đủ nhiều" (P3, `evidence/interviews/P3.md`)

Data BTC không có câu chữ học viên viết về lab (`chat.csv` cột `transcript` chỉ là tên file video), nên trích dẫn nguyên văn chỉ lấy được từ phỏng vấn.

## 4. Các nguồn có khớp nhau không

- **Data nói:** hơn 1/3 lượt mở lab không xong, và phần lớn dừng rất sớm (bước 0, khoảng 2 phút). Data cho biết *dừng ở đâu*, không cho biết *vì sao*.
- **Người dùng nói (P4):** dừng vì lỗi môi trường (Docker, server), không phải vì không hiểu bước tiếp theo, và đã mất ~60 phút trước khi bỏ. P4 muốn được gợi ý thay vì nhận đáp án, khớp với thiết kế gợi ý theo cấp ở `spec.md` §4.
- **Người dùng nói (P1):** kẹt ở bước vẽ sơ đồ quy trình hiện tại của mini lab số 2, đã tìm trên mạng và dùng AI, mất ~20 phút rồi dừng vì **hết thời gian**. P1 muốn "gợi ý trước rồi đến đáp án".
- **Người dùng nói (P3):** khó hiểu cấu trúc file và yêu cầu của lab Day 14, đã dùng AI để tóm tắt yêu cầu và định hướng cách làm, mất ~25–30 phút. P3 cho rằng lab ngày càng khó trong khi thời gian thực hành không đủ.
- **Khớp:** cả P1, P3 và P4 đều kẹt thật ở một chỗ và loay hoay 20–60 phút. P1 và P3 đều đã dùng AI để tự gỡ, tức là học viên đã quen hỏi AI khi kẹt. P1 và P4 muốn gợi ý trước thay vì nhận đáp án ngay.
- **Lệch:**
  - Không ai coi kẹt là lý do chính: P1 và P3 rơi vào cách giải thích (a) thiếu thời gian (P3 kèm thêm "lab ngày càng khó"), P4 rơi vào (c) lỗi kỹ thuật trong `evidence/hypothesis.md`. Có thể đây là cùng một chuỗi: kẹt làm tốn thời gian, rồi hết giờ thì bỏ.
  - P1 cuối cùng vẫn muốn có đáp án, trong khi thiết kế ở `spec.md` §4 không bao giờ đưa lời giải.
  - Chỗ P3 kẹt là hiểu yêu cầu và cấu trúc dự án, không hẳn là "không biết bước tiếp theo". Chưa xác nhận P3 có bỏ lab hay không, và lab Day 14 có phải mini lab pre-class hay không.
  - Lượt bỏ qua ở bước 0 sau khoảng 2 phút (59/98) không khớp với kiểu loay hoay 20–60 phút của P1, P3 và P4. Có thể là hai nhóm hành vi khác nhau; phỏng vấn chưa giải thích được nhóm bỏ qua sớm.

## 5. Kết luận

Giả thuyết ở `evidence/hypothesis.md`: **phải đổi**. Ngưỡng đặt trước là ≥2/3 người phỏng vấn kẹt ở một bước **và** kẹt là lý do chính. Cả 3 người (P1, P3, P4) đều kẹt ở một chỗ, nhưng 0/3 coi kẹt là lý do chính: P1 và P3 nói thiếu thời gian, P4 nói lỗi môi trường. Vì vậy vế "kẹt là lý do chính" không đạt. Kể cả nếu P2 đạt cả hai vế thì cũng chỉ được 1/4, vẫn dưới ngưỡng.

Giả thuyết sửa lại: kẹt ở một bước là chuyện phổ biến và làm học viên mất 20–60 phút. Thời gian đó cộng với lịch học dày khiến học viên hết giờ rồi bỏ. Gợi ý bước tiếp theo có giá trị ở chỗ **rút ngắn thời gian kẹt**, chứ không phải gỡ một lý do bỏ lab riêng biệt. Lỗi môi trường (P4) nằm ngoài lát cắt này.

Điều vẫn chưa biết:
- Lượt bỏ qua ở bước 0 là do kẹt, thiếu thời gian, hay coi lab là không bắt buộc?
- Thời gian mất mỗi lần kẹt dao động 20–60 phút (n=3: P1 ~20, P3 ~25–30, P4 ~60), trung vị ~25–30 phút. `spec.md` §2 đang dùng 40 phút (trung vị của n=2), cần tính lại.
- Lỗi môi trường chiếm bao nhiêu phần? Nếu nhiều thì lát cắt gợi ý bước tiếp theo phải biết nói "việc này ngoài phạm vi, hỏi lab coach".

## Lịch hẹn (chỉ ghi vai và giờ, không ghi tên)

| Vai | Người hỏi | Giờ hẹn | Đã xong? |
|---|---|---|---|
| Học viên ngoài nhóm | Minh (P1) | 27/11 | ☑ |
| Học viên L3 | Huy (P3) | 28/11 09:27 (qua tin nhắn) | ☑ |
| Học viên ngoài nhóm | Hùng (P4) | 27/11 | ☑ |
