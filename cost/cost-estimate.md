# Ước tính chi phí vận hành trợ giảng mini lab pre-class

## 1. Phạm vi và cơ sở tính toán

Hệ thống hỗ trợ học viên nhận gợi ý theo từng bước mini lab; AI không làm hoặc nộp bài thay học viên. Chi phí được ước tính theo số phiên hỗ trợ, số lượt hỏi trong mỗi phiên và số token mà mô hình thực tế xử lý.

Các nguồn sử dụng:

- Thống kê hành vi: `evidence/data-mining.md`, phương pháp tái lập trong `evidence/count.py`.
- Giả định nhóm người dùng và bảng giá: `cost/personas.yaml`.
- Lượng token thực đo: `cost/simulate-N.csv` và `cost/simulate-N-summary.md` sau khi chạy mô phỏng bằng model thật.
- Tỷ lệ câu trả lời đạt: báo cáo đánh giá lượt 2 của `eval/run-2.csv` đã được người chấm xác nhận.

### Cơ sở dữ liệu hành vi đã xác minh

Trong giai đoạn 05–25/11/2026, có 538 cặp học viên–lab đã mở; 194 cặp không hoàn thành (36,1%). Có 147 học viên đã mở ít nhất một lab và 107 người trong nhóm này từng không hoàn thành ít nhất một lab.

Nếu quy đổi **số lab không hoàn thành** từ 21 ngày sang 30 ngày, tổng quy mô là khoảng `194 × 30/21 = 277` cặp học viên–lab/tháng; trung bình khoảng `277/147 = 1,89` cặp không hoàn thành/học viên đã mở lab/tháng. Đây là **chỉ số hành vi đại diện**, không phải số phiên chat AI thực tế hoặc nhu cầu chắc chắn sẽ phát sinh. Không thể suy ra phân bố ba persona chỉ từ giá trị trung bình này.

## 2. Giả định mô phỏng và mức độ kiểm chứng

| Thành phần | Cách xác định | Trạng thái |
|---|---|---|
| 3 persona: dùng ít, vừa, nhiều | Tỷ trọng 50%/30%/20%; 1/2/4 phiên/người/tháng; 1/2/3 lượt hỏi/phiên | **Giả định để mô phỏng**, chưa có số đo sử dụng AI thực tế |
| Quy mô thấp / cơ sở / cao | 50 / 107 / 147 người trong `cost/personas.yaml` | 50: tự ước tính; 107 người từng không hoàn thành lab; 147 người từng mở lab. **Chưa chứng minh tất cả sẽ dùng AI** |
| Hai mức giá model | Gemini 3.1 Flash-Lite và Gemini 2.5 Pro; USD/1 triệu token | Theo Google Gemini API Standard Paid Tier, https://ai.google.dev/gemini-api/docs/pricing (28/11/2026); Pro là phương án áp giá so sánh |
| Model dùng để đo token | `gemini-3.1-flash-lite` | Có token thật trong lượt mô phỏng thử 10 phiên; chưa có số đo chính thức ≥50 phiên |
| Tỷ lệ đạt | Lấy từ lượt đánh giá chính thức đã chấm | **Chưa có `eval/run-2.csv` đã chấm**; không lấy kết quả thống nhất 5 câu giữa hai người chấm thay thế |
| Phỏng vấn học viên P4 | `evidence/interviews/P4.md` | Đã phỏng vấn: lỗi Docker và server khiến học viên không hoàn thành lab; mất khoảng 60 phút; tự báo gặp 1 lần/tháng |

Các giả định dùng để mô phỏng phải được ghi rõ nguồn; nếu dựa vào phỏng vấn thì trỏ tới P1–P4, nếu chưa có bằng chứng thì ghi **tự ước tính**. Không thay số nhằm khớp một kết luận có sẵn.

**Đối chiếu P4:** Học viên cho biết gặp khó khăn khoảng 1 lần/tháng và mất khoảng 60 phút xử lý sự cố Docker/server. Đây là một trường hợp định tính; không thể suy trực tiếp số lần hỏi AI hoặc thời gian AI tiết kiệm được.

**Mô phỏng thử:** Theo kết quả chạy ngày 27/11/2026, `python run.py simulate --try --wait 4` hoàn tất 10/10 phiên, 0 lỗi trên `gemini-3.1-flash-lite`; S008 và S010 không phát sinh token. Kết quả này dùng để xác nhận khả năng chạy, **không thay thế mô phỏng ≥50 phiên**. Các số chi phí tháng phải tính lại sau khi cập nhật persona; chưa có tỷ lệ đạt từ lượt eval đã chấm.


## 3. Phương pháp tính

- **Chi phí mỗi lượt gọi** = `(token_đầu_vào × giá_đầu_vào + token_đầu_ra × giá_đầu_ra) / 1.000.000` (USD).
- **Chi phí mỗi phiên** = tổng chi phí các lượt gọi model trong phiên.
- **Chi phí trung bình mỗi phiên** = tổng chi phí các phiên không lỗi / số phiên không lỗi.
- **Chi phí ước tính mỗi câu/task đạt** = chi phí trung bình tương ứng / tỷ lệ đạt đã đánh giá, nếu tỷ lệ đạt lớn hơn 0. Tỷ lệ đạt đo trên **câu thử**, không chứng minh toàn bộ phiên học đã hoàn thành thành công.
- **Chi phí mỗi tháng theo quy mô** = tổng trên các persona của `(số người dùng × tỷ trọng persona × số phiên/người/tháng × chi phí trung bình mỗi phiên của persona)`.

Hai model trong bảng giá có thể là kịch bản thay thế. Nếu **đo token ở model X nhưng áp giá model Y**, phải ghi rõ đây là ước tính chéo model: cách token hóa và số token đầu ra có thể khác nhau.

## 4. Bảng kết quả cần điền sau khi có số đo

Thông tin chạy chính thức: `cost/simulate-N.csv` — **chưa có lượt ≥50 phiên và tỷ lệ đạt từ eval đã chấm để kết luận**.

| Model áp giá | Chi phí/phiên (USD) | Chi phí/task đạt (USD) | Thấp (USD/tháng) | Cơ sở (USD/tháng) | Cao (USD/tháng) | Chi phí/người/tháng (USD) |
|---|---:|---:|---:|---:|---:|---:|
| Model giá thấp | Chưa đo | Chưa tính | Chưa tính | Chưa tính | Chưa tính | Chưa tính |
| Model giá cao | Chưa đo | Chưa tính | Chưa tính | Chưa tính | Chưa tính | Chưa tính |

Không lấy token 0 từ chế độ `fake` để tính chi phí vận hành. Lần mô phỏng chính thức cần ít nhất **50 phiên không thay thế bằng lượt giả**, ghi số phiên lỗi và trỏ tới bản tóm tắt được công cụ xuất ra.

## 5. Đối chiếu chi phí với tác động

Ước tính tác động tại `spec.md` §2 đang dùng 20 phút/lượt không hoàn thành, tương đương khoảng 92 giờ/tháng cho toàn nhóm hành vi được xét. **20 phút là giả định chưa được phỏng vấn xác nhận**; 92 giờ/tháng cũng không phải thời gian đã chứng minh hệ thống sẽ tiết kiệm được.

Kết luận về tính đáng triển khai chỉ được đưa ra sau khi có (1) thời gian mất thêm hoặc tác động được phỏng vấn kiểm chứng, (2) số phiên và token thực đo, (3) tỷ lệ đạt của lượt đánh giá cuối, và (4) giả định tỷ lệ sử dụng thực tế. Giá model chỉ phản ánh một phần chi phí; chưa bao gồm lưu trữ, triển khai, vận hành và giám sát.

## 6. Minh chứng cần hoàn thiện trước CP4

- `python run.py simulate --try`: đã chạy 10/10 phiên không lỗi với Gemini 3.1 Flash-Lite; cần lưu CSV và trace làm minh chứng, chạy lại nếu thay cấu hình persona.
- `eval/run-2.csv`: nhận từ Huy sau khi đã chấm, kèm thống kê theo metric và model thực sử dụng.
- `python run.py simulate --rate-from eval/run-2.csv`: mô phỏng ít nhất 50 phiên, lưu CSV và báo cáo tự sinh.
- `cost/personas.yaml`: đã có 3 persona, nguồn giả định, 3 kịch bản quy mô và giá 2 model; cần chốt cấu hình trước mô phỏng chính thức.
- Cập nhật `spec.md` §8 từ bảng kết quả thực tế, có ghi nguồn và hạn chế.
