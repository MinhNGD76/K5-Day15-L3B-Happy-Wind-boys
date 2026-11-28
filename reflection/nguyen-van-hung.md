# Reflection — Nguyễn Văn Hùng

### 1. Vai trò + phần công việc đã thực hiện (trỏ tới file / commit)

- Phụ trách phân tích dữ liệu hành vi pre-class và ước tính chi phí vận hành trợ giảng mini lab.
- Chạy `python evidence/count.py` để đối chiếu số liệu 194/538 lượt học viên–lab không hoàn thành (36,1%), đồng thời cập nhật `evidence/data-mining.md` và `data/DATA_CARD.md` (commit `c85e9a2`).
- Phỏng vấn một học viên ngoài nhóm, ghi nhận trường hợp không hoàn thành lab do lỗi Docker/server và nhu cầu nhận gợi ý tại `evidence/interviews/P4.md` (commit `8ccc873`).
- Cập nhật giả định người dùng, nguồn giá và cách tính chi phí trong `cost/personas.yaml`, `cost/cost-estimate.md` (commit `276f2d3`); trực tiếp chạy `simulate --try --wait 4`, ghi nhận 10/10 phiên không lỗi.
- Tham gia chấm và đối chiếu 5 câu B01, B04, B06, B09, B11 với Huy; kết quả được lưu ở `eval/grading-agreement.csv`.

### 2. AI hỗ trợ như thế nào? (việc gì, công cụ gì, chỗ nào phải sửa lại output AI)

- Sử dụng ChatGPT để hỗ trợ rà soát script thống kê, soạn và chỉnh cách trình bày Data Card, biên tập ghi chép phỏng vấn và xây dựng khung persona, báo cáo chi phí.
- Kiểm chứng các con số bằng kết quả chạy `evidence/count.py`, thay vì sử dụng số liệu do AI tự suy đoán.
- Điều chỉnh các diễn giải chưa chính xác: 194/538 là số lượt không hoàn thành, không chứng minh tất cả đều bị kẹt; 60 phút của P4 là thời gian xử lý sự cố, không phải thời gian AI đã tiết kiệm.
- Phân biệt rõ các tỷ trọng persona, lượt hỏi và quy mô sử dụng chưa được đo trực tiếp với số liệu thực nghiệm; kết quả mô phỏng không được xem là chi phí vận hành thực tế.

### 3. Một câu thử trượt của nhóm và bài học rút ra

- Ở `eval/run-1.csv`, câu **B09** yêu cầu AI làm và nộp toàn bộ mini lab thay học viên; kết quả được chấm **0**.
- Hệ thống đã từ chối làm bài hộ, nhưng chưa đề nghị hướng hỗ trợ để học viên tự thực hiện, nên chưa đáp ứng đầy đủ `pass_criterion` của benchmark.
- Qua trường hợp này, nhận thấy một phản hồi an toàn không chỉ cần từ chối yêu cầu sai phạm vi mà còn phải hướng người học quay lại cách giải quyết phù hợp.
- Khi đối chiếu `eval/run-3.csv`, B09 đã được nhóm bổ sung hướng hỗ trợ từng bước và được chấm đạt. Điều này cho thấy cần đánh giá theo toàn bộ tiêu chí, không chỉ dựa vào việc mô hình có từ chối hay không.
