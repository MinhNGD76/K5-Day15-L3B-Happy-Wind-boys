# Reflection — Nguyễn Tài Minh Huy

## 1. Vai trò + phần mình làm (trỏ tới file / commit):

- Em phụ trách Evaluation và Failure Analysis, xây dựng bộ benchmark từ 12 lên 24 câu thử và xác định 4 metric đánh giá cùng ngưỡng đạt.
- Em tham gia chấm kết quả, kiểm tra safety tests và phân tích 5 câu thử chưa đạt trong baseline CP3.
- Em thực hiện phỏng vấn P3 để thu thập bằng chứng về khó khăn của học viên khi làm lab.
- Em phối hợp với các thành viên để cải tiến hệ thống và đánh giá kết quả trước và sau cải tiến.
- File đóng góp: `eval/benchmark.csv`, `eval/metric_spec.yaml`, `eval/report.md`, `eval/README.md`, `spec.md` §5, §7, §10 và `evidence/interviews/P3.md`.
- Commit tiêu biểu: `ba5a644`, `52d4838`.

## 2. AI hỗ trợ mình thế nào (việc gì, công cụ gì, chỗ nào phải sửa lại output AI):

- Em sử dụng ChatGPT để hỗ trợ phân tích yêu cầu, xây dựng benchmark, đề xuất tiêu chí đánh giá và phân tích nguyên nhân các câu thử trượt.
- AI cũng hỗ trợ viết lệnh PowerShell, kiểm tra Git và xử lý merge conflict khi tích hợp công việc của các thành viên.
- Em phải điều chỉnh các câu thử để phù hợp với dữ liệu synthetic V2 và bảo toàn những câu thử đã được chốt ở CP2.
- Khi phân tích kết quả, em không sử dụng trực tiếp mọi đề xuất của AI mà đối chiếu với output thực tế và tiêu chí chấm.
- Em nhận thấy AI giúp tiết kiệm thời gian, nhưng con người vẫn phải chịu trách nhiệm kiểm chứng dữ liệu, kết quả và quyết định cuối cùng.

## 3. Một câu thử trượt của nhóm và mình học được gì từ nó:

- Câu B08: học viên đã mở mini lab nhưng chưa hoàn thành và không biết tiếp tục như thế nào.
- Trong baseline CP3, Agent tự hướng dẫn học viên bắt đầu từ bước 1 mặc dù chưa biết tiến độ thực tế.
- Câu này bị chấm trượt vì Agent cần hỏi bước hiện tại hoặc những cách học viên đã thử trước khi đưa ra gợi ý.
- Sau cải tiến CP4, Agent đã hỏi lại tiến độ thay vì tự suy đoán, giúp câu B08 chuyển từ FAIL sang PASS trong run-3.
- Em học được rằng một câu trả lời có vẻ hợp lý chưa chắc đã đáp ứng đúng nhu cầu người dùng. Agent cần biết khi nào nên hỏi lại thay vì tự đưa ra giả định.
- Việc giữ nguyên benchmark và tiêu chí chấm giúp nhóm đo lường hiệu quả cải tiến một cách nhất quán và trung thực.
