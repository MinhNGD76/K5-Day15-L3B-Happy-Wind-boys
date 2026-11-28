# Ước tính chi phí vận hành trợ giảng mini lab pre-class

> Phụ trách: Nguyễn Văn Hùng. Cập nhật CP4 28/11/2026. Số trong bảng chép từ `cost/simulate-2-summary.md` (khung tự sinh, không sửa tay).

## 1. Phạm vi và cơ sở tính toán

Hệ thống đưa một gợi ý bước tiếp theo cho học viên đang kẹt mini lab. AI không làm hoặc nộp bài thay học viên. Chi phí tính theo số phiên hỗ trợ, số lượt hỏi mỗi phiên và số token model thật xử lý.

| Nguồn | Dùng cho |
|---|---|
| `evidence/data-mining.md`, `evidence/count.py` | Quy mô hành vi: 194/538 lượt mở lab không xong, 107/147 học viên có ≥1 lab không xong |
| `cost/personas.yaml` | 3 persona, 3 kịch bản số người dùng, giá 2 model |
| `cost/simulate-2.csv`, `cost/simulate-2-summary.md`, `traces/simulate-2.jsonl` | Token, số lần gọi model và công cụ, đo bằng model thật trên agent bản CP4 |
| `eval/run-3.csv` | Tỉ lệ đạt 23/24 (96%): lượt sau cải tiến, đã chấm |
| `spec.md` §2 | Impact ~127 giờ học viên / tháng |

## 2. Giả định mô phỏng và mức độ kiểm chứng

| Thành phần | Giá trị | Trạng thái |
|---|---|---|
| 3 persona: dùng ít, vừa, nhiều | Tỉ trọng 50% / 30% / 20%; 1 / 2 / 4 phiên / người / tháng; 1 / 2 / 3 lượt hỏi / phiên | *(tự ước tính)*. Mức thấp nhất khớp phỏng vấn: P1 và P4 tự báo ~1 lần kẹt / tháng |
| Số người dùng: thấp / cơ sở / cao | 50 / 107 / 147 | 50: *(tự ước tính)*. 107: học viên từng có lab không xong. 147: học viên từng mở lab (`evidence/data-mining.md`). Chưa chứng minh tất cả sẽ dùng AI |
| Giá model (USD / 1 triệu token) | gemini-3.1-flash-lite: vào 0,25 · ra 1,50. gemini-2.5-pro: vào 1,25 · ra 10,00 | Google Gemini API Standard Paid Tier, https://ai.google.dev/gemini-api/docs/pricing, tra 28/11/2026 |
| Model đo token | `gemini-3.1-flash-lite` (đúng `MODEL_NAME` trong `.env`) | Đo thật. Giá gemini-2.5-pro là **áp giá chéo**: đo token trên Flash-Lite, tính theo giá Pro. Bộ tách token và độ dài output của Pro có thể khác |
| Tỉ lệ đạt | 23/24 (96%), `run-3@20261128-141616` | Đã chấm. Câu trượt duy nhất (B01) là lỗi kỹ thuật timeout |

## 3. Phương pháp tính

- **Chi phí mỗi lượt gọi** = (token vào × giá vào + token ra × giá ra) / 1.000.000 (USD).
- **Chi phí trung bình mỗi phiên** = tổng chi phí các phiên không lỗi / số phiên không lỗi.
- **Chi phí / task thành công** = chi phí / phiên ÷ tỉ lệ đạt.
- **Chi phí / tháng** = tổng theo persona của (số người × tỉ trọng × phiên / người / tháng × chi phí / phiên của persona).

## 4. Kết quả: `simulate-2@20261128-143612`

Lệnh: `python run.py simulate --rate-from eval/run-3.csv --wait 4`. 50 phiên, seed 42. **46/50 phiên chạy xong, 4/50 phiên lỗi** (S006, S015, S020, S029, đều là `TimeoutError` khi gọi model). Phiên lỗi không tính vào trung bình.

| Persona | Số phiên | Lượt hỏi / phiên | Token vào / phiên | Token ra / phiên | Gọi model / phiên | Gọi công cụ / phiên |
|---|---:|---:|---:|---:|---:|---:|
| dung_it | 23 | 1 | 417 | 45 | 0,6 | 2,1 |
| dung_vua | 14 | 2 | 860 | 98 | 1,1 | 4,4 |
| dung_nhieu | 9 | 3 | 1205 | 138 | 1,7 | 6,7 |

Số lần gọi model mỗi phiên nhỏ hơn số lượt hỏi, vì câu xin đáp án, injection, lab không tồn tại hay thiếu tiến độ được code xử lý mà không gọi model.

| Model áp giá | Chi phí / phiên | Chi phí / task thành công | Thấp · 50 người (USD / tháng) | Cơ sở · 107 người (USD / tháng) | Cao · 147 người (USD / tháng) | Chi phí / người / tháng (cơ sở) |
|---|---:|---:|---:|---:|---:|---:|
| gemini-3.1-flash-lite (đang dùng) | $0,00030 | $0,00031 | $0,036 | $0,076 | $0,104 | $0,00071 |
| gemini-2.5-pro (áp giá chéo) | $0,0017 | $0,0017 | $0,20 | $0,43 | $0,59 | $0,0040 |

**Phóng lên quy mô khoá** *(tự ước tính, tuyến tính theo chi phí / người / tháng ở kịch bản cơ sở)*: nếu cả lớp L3 (hơn 700 học viên, theo đề) đều dùng như persona, khoảng **$0,50 / tháng** với Flash-Lite và **$2,8 / tháng** với Pro.

So với lượt trước: `simulate-1` (agent bản CP3, tỉ lệ đạt run-2 79%, 0/50 lỗi) ra $0,00042 / task thành công và $0,087 / tháng ở kịch bản cơ sở. Bản CP4 rẻ hơn một chút vì tỉ lệ đạt cao hơn và có thêm nhánh hỏi lại không cần gọi model.

## 5. Đối chiếu chi phí với tác động

- **Impact** (`spec.md` §2): ~127 giờ học viên / tháng (277 lượt lab không xong × 27,5 phút, trung vị phỏng vấn n=3). Chia cho 107 người ở kịch bản cơ sở: **~1,2 giờ / người / tháng** (mức trần).
- **Chi phí:** dưới $0,001 / người / tháng với Flash-Lite, $0,004 với Pro.
- **Kết luận:** đáng làm xét về chi phí model, kể cả với model đắt. Chi phí không phải nút thắt. Thứ quyết định là gợi ý có rút ngắn thời gian kẹt thật không (chưa đo với người dùng), và độ ổn định khi gọi model (dưới đây).

## 6. Hạn chế

- **Timeout 4/50 phiên (8%)**: cùng loại lỗi làm B01 trượt ở `run-3`. Khi dùng thật, cứ khoảng 12 phiên có 1 học viên không nhận được trả lời. Cần thêm thử lại khi timeout trước khi pilot. Lỗi này không làm tăng chi phí đáng kể.
- Persona, tỉ trọng và số phiên / tháng là *(tự ước tính)*, chưa có số đo học viên dùng AI thật.
- Câu hỏi trong mô phỏng lấy từ bộ câu thử, trên 3 lab synthetic. Đề lab thật dài hơn thì token vào sẽ tăng theo.
- Chỉ tính tiền model. Chưa tính hosting, giám sát, giờ công lab coach viết và duyệt đề lab cùng thang gợi ý. Phần giờ công nhiều khả năng lớn hơn tiền model nhiều lần.
