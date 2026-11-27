# Data Card — dữ liệu cho hệ thống hỗ trợ mini lab pre-class

## 1. Mục đích và phạm vi

Hai nguồn dữ liệu phục vụ hai mục đích khác nhau:

- **Dữ liệu synthetic:** làm tri thức tham chiếu cho bản chạy thử gợi ý từng bước; không đại diện cho đề lab chính thức của khóa học.
- **Dữ liệu hành vi pre-class:** phân tích tình trạng mở, hoàn thành, bỏ qua hoặc bỏ dở mini lab để xác định quy mô vấn đề và xây dựng giả định sử dụng. Dữ liệu hành vi không được dùng làm lời giải hay đưa nguyên bản vào yêu cầu gửi tới mô hình.

## 2. Dataset 1 — Bộ minh họa mini lab (synthetic)

| Thuộc tính | Mô tả |
|---|---|
| Tệp | `data/labs.json` |
| Nguồn | Nội dung minh họa do nhóm xây dựng với sự hỗ trợ của công cụ AI; **không phải dữ liệu BTC, không phải đề lab chính thức**. |
| Nhãn nguồn | `synthetic` |
| Quy mô | 8 bước trong các mini lab minh họa về prompt và LLM. |
| Cấu trúc | Mã/tên lab, nội dung bước, gợi ý và dữ liệu hỗ trợ luồng tra cứu theo bước (theo các trường được khai báo trong JSON). |
| Xử lý | Biên soạn nội dung ngắn theo phạm vi bài toán A6; không sử dụng thông tin định danh học viên. |
| Phiên bản | `synthetic-prompt-lab-v1`, ngày 27/11/2026. |
| Ứng dụng | Dữ liệu đầu vào cho công cụ truy xuất bước lab của bản chạy thử. |
| Hạn chế | Không chứng minh được độ khó, đáp án hay hiệu quả hỗ trợ đối với mini lab chính thức. |

**Kiểm duyệt nội dung:** Phạm Lê Chuẩn là người được phân công xác nhận nội dung lab theo thiết kế tại `spec.md` §4. Trạng thái xác nhận thủ công: **chưa có bằng chứng ký xác nhận**. Người phụ trách tài liệu dữ liệu: Nguyễn Văn Hùng.

## 3. Dataset 2 — Dữ liệu hành vi pre-class (BTC cung cấp)

| Thuộc tính | Mô tả |
|---|---|
| Nguồn | Dữ liệu pre-class do Ban tổ chức cung cấp. |
| Vị trí xử lý nội bộ | `data-btc/preclass/` (không đưa vào Git). |
| Tệp | `events.csv`, `chat.csv`, `answers.csv`. |
| Loại dữ liệu | Nhật ký hành vi và tương tác trong môi trường học tập; các bản ghi dùng mã học viên, không sử dụng tên thật trong báo cáo. |
| Thời gian phân tích | 05–25/11/2026 (21 ngày), theo phạm vi ghi trong `evidence/data-mining.md`. |
| Đơn vị thống kê chính | Cặp `(hv, lab_key)` có ít nhất một sự kiện `lab_opened`; mở lại cùng lab không tính thành lượt mới. |
| Quy tắc phân loại | Hoàn thành thật nếu có `lab_completed` không bỏ qua; chỉ bỏ qua nếu mọi sự kiện hoàn thành đều có `skipped=true`; bỏ dở nếu không ghi nhận sự kiện hoàn thành. |
| Công cụ tái lập | `python evidence/count.py`, sử dụng `events.csv` và `chat.csv` cho các chỉ số in ra. |
| Mục đích sử dụng | Định lượng tình trạng không hoàn thành mini lab và mô tả hành vi; hỗ trợ xây dựng giả định về nhu cầu, **không đo trực tiếp số lần học viên sẽ hỏi AI**. |
| Quyền riêng tư | Không commit CSV gốc, không đưa câu chat cá nhân vào repository, chỉ công bố số tổng hợp và ví dụ đã mã hóa. |

### Kết quả tổng hợp từ dữ liệu hành vi

| Chỉ số | Kết quả |
|---|---:|
| Học viên có hoạt động | 436 |
| Học viên từng mở ít nhất một lab | 147 |
| Cặp học viên × lab đã mở | 538 |
| Hoàn thành thực sự | 344/538 (63,9%) |
| Chỉ bỏ qua | 98/538 (18,2%) |
| Bỏ dở, không có sự kiện kết thúc | 96/538 (17,8%) |
| Không hoàn thành thực sự (bỏ qua hoặc bỏ dở) | **194/538 (36,1%)** |
| Học viên đã mở lab có ít nhất một lab không hoàn thành | 107/147 (72,8%) |

Nguồn kết quả: `evidence/count.py`, tái chạy trên dữ liệu pre-class ngày **27/11/2026**. Các số liệu trên phản ánh hành vi ghi nhận trong hệ thống; **không chứng minh rằng toàn bộ 194 trường hợp đều bị kẹt**.

`answers.csv` đã được xác nhận có trong thư mục dữ liệu nội bộ, nhưng **không được đọc bởi `evidence/count.py`**. Mọi chỉ số lấy riêng từ `answers.csv` cần được kiểm tra bằng phương pháp riêng trước khi coi là đã tái xác minh.

### Giới hạn và rủi ro diễn giải

- Không có sự kiện hoàn thành có thể do học viên bỏ dở, quên ghi nhận hoặc làm ở môi trường khác.
- Bỏ qua ở bước 0 chưa đủ bằng chứng kết luận học viên gặp khó khăn kỹ thuật.
- Số người có bản ghi trong `chat.csv` không đồng nghĩa số người đã hỏi trợ giảng AI: phải lọc đúng kênh và loại tương tác trước khi dùng chỉ số này.
- Tần suất không hoàn thành lab **không phải** tần suất sử dụng AI. Giả định về số phiên AI và số lượt hỏi phải có nguồn riêng hoặc ghi rõ là ước tính.
- Kết luận về nguyên nhân và thời gian mất thêm cần được bổ sung từ phỏng vấn P1–P4; không tự suy diễn từ log hành vi.

## 4. Quản lý và kiểm tra dữ liệu

- Bản gốc do nhóm giữ trong thư mục nội bộ đã loại khỏi Git; chỉ đưa vào repository script, tài liệu phương pháp và số tổng hợp.
- Khi dữ liệu BTC được cập nhật, chạy lại `evidence/count.py` và ghi rõ ngày cùng phạm vi trước khi sử dụng số mới.
- Bộ synthetic phải được kiểm tra về tính chính xác nội dung, dấu hiệu lộ lời giải và tính phù hợp với `spec.md` §4 trước demo.
