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
| 3 persona: dùng ít, vừa, nhiều | Tỷ trọng, số phiên/người/tháng, số lượt hỏi/phiên trong `cost/personas.yaml` | Các số đang có là **giả định ban đầu**, chưa được xác nhận bằng phỏng vấn hoặc phân bố theo học viên |
| Quy mô thấp / cơ sở / cao | `users.low`, `users.base`, `users.high` | Cần đối chiếu quy mô lớp và giả định tỷ lệ sử dụng; không đồng nhất tổng tài khoản với người chắc chắn dùng AI |
| Hai mức giá model | Giá vào và ra, USD/1 triệu token | Cần xác nhận model sẽ dùng và nguồn giá của đúng nhà cung cấp API tại thời điểm chạy |
| Model dùng để đo token | Trường `model` do API trả về | **Chưa có bản đo token thật được xác nhận** |
| Tỷ lệ đạt | Lấy từ lượt đánh giá chính thức đã chấm | **Chưa có `eval/run-2.csv` đã chấm**; không lấy kết quả thống nhất 5 câu giữa hai người chấm thay thế |
| Phỏng vấn học viên P4 | Một học viên ngoài nhóm, ghi nguyên văn tình huống đã xảy ra | **Chưa thực hiện phỏng vấn** |

Các giả định dùng để mô phỏng phải được ghi rõ nguồn; nếu dựa vào phỏng vấn thì trỏ tới P1–P4, nếu chưa có bằng chứng thì ghi **tự ước tính**. Không thay số nhằm khớp một kết luận có sẵn.

## 3. Phương pháp tính

- **Chi phí mỗi lượt gọi** = `(token_đầu_vào × giá_đầu_vào + token_đầu_ra × giá_đầu_ra) / 1.000.000` (USD).
- **Chi phí mỗi phiên** = tổng chi phí các lượt gọi model trong phiên.
- **Chi phí trung bình mỗi phiên** = tổng chi phí các phiên không lỗi / số phiên không lỗi.
- **Chi phí ước tính mỗi câu/task đạt** = chi phí trung bình tương ứng / tỷ lệ đạt đã đánh giá, nếu tỷ lệ đạt lớn hơn 0. Tỷ lệ đạt đo trên **câu thử**, không chứng minh toàn bộ phiên học đã hoàn thành thành công.
- **Chi phí mỗi tháng theo quy mô** = tổng trên các persona của `(số người dùng × tỷ trọng persona × số phiên/người/tháng × chi phí trung bình mỗi phiên của persona)`.

Hai model trong bảng giá có thể là kịch bản thay thế. Nếu **đo token ở model X nhưng áp giá model Y**, phải ghi rõ đây là ước tính chéo model: cách token hóa và số token đầu ra có thể khác nhau.

## 4. Bảng kết quả cần điền sau khi có số đo

Thông tin chạy: `cost/simulate-N.csv` — **chưa có số đo hợp lệ để kết luận**.

| Model áp giá | Chi phí/phiên (USD) | Chi phí/task đạt (USD) | Thấp (USD/tháng) | Cơ sở (USD/tháng) | Cao (USD/tháng) | Chi phí/người/tháng (USD) |
|---|---:|---:|---:|---:|---:|---:|
| Model giá thấp | Chưa đo | Chưa tính | Chưa tính | Chưa tính | Chưa tính | Chưa tính |
| Model giá cao | Chưa đo | Chưa tính | Chưa tính | Chưa tính | Chưa tính | Chưa tính |

Không lấy token 0 từ chế độ `fake` để tính chi phí vận hành. Lần mô phỏng chính thức cần ít nhất **50 phiên không thay thế bằng lượt giả**, ghi số phiên lỗi và trỏ tới bản tóm tắt được công cụ xuất ra.

## 5. Đối chiếu chi phí với tác động

Ước tính tác động tại `spec.md` §2 đang dùng 20 phút/lượt không hoàn thành, tương đương khoảng 92 giờ/tháng cho toàn nhóm hành vi được xét. **20 phút là giả định chưa được phỏng vấn xác nhận**; 92 giờ/tháng cũng không phải thời gian đã chứng minh hệ thống sẽ tiết kiệm được.

Kết luận về tính đáng triển khai chỉ được đưa ra sau khi có (1) thời gian mất thêm hoặc tác động được phỏng vấn kiểm chứng, (2) số phiên và token thực đo, (3) tỷ lệ đạt của lượt đánh giá cuối, và (4) giả định tỷ lệ sử dụng thực tế. Giá model chỉ phản ánh một phần chi phí; chưa bao gồm lưu trữ, triển khai, vận hành và giám sát.

## 6. Minh chứng cần hoàn thiện trước CP4

- `python run.py simulate --try`: xác nhận model thật, token được đo, 0 phiên lỗi hoặc nêu rõ lỗi.
- `eval/run-2.csv`: nhận từ Huy sau khi đã chấm, kèm thống kê theo metric và model thực sử dụng.
- `python run.py simulate --rate-from eval/run-2.csv`: mô phỏng ít nhất 50 phiên, lưu CSV và báo cáo tự sinh.
- `cost/personas.yaml`: xác minh model, bảng giá và nguồn giả định; bổ sung kết quả phỏng vấn P4 khi có.
- Cập nhật `spec.md` §8 từ bảng kết quả thực tế, có ghi nguồn và hạn chế.
