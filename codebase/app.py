"""Giao diện web tối giản cho bản demo trợ giảng mini lab.

Chạy bằng `python run.py`. Server chỉ lắng nghe trên máy hiện tại và dùng
HTTP server trong thư viện chuẩn; nội dung trả lời vẫn đi qua agent.answer().
"""
import json
import os
import sys
import webbrowser
from http.server import BaseHTTPRequestHandler, HTTPServer

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import ai  # noqa: E402
import tracing  # noqa: E402
from agent import answer  # noqa: E402


HOST = "127.0.0.1"
PORT = 8000
MAX_BODY = 12_000

PAGE = r"""<!doctype html>
<html lang="vi">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="theme-color" content="#f7f8fc">
<title>Trợ giảng mini lab · HappyWindBoys</title>
<style>
:root{font-family:Inter,"Segoe UI",Arial,sans-serif;color:#17212b;background:#f7f8fc;font-synthesis:none}
*{box-sizing:border-box}body{margin:0;min-height:100vh;background:radial-gradient(ellipse at 50% -15%,#dcefeb 0,transparent 48%),#f7f8fc}
.shell{max-width:1040px;margin:0 auto;padding:26px 24px 34px}.top{display:flex;align-items:center;justify-content:space-between;gap:16px;margin-bottom:20px}
.brand{display:flex;align-items:center;gap:12px}.logo{display:grid;place-items:center;width:42px;height:42px;border-radius:14px;background:#0b6e69;color:white;font-size:21px;font-weight:800;box-shadow:0 7px 18px #0b6e6928}
.brand strong{display:block;font-size:15px;letter-spacing:.01em}.brand span{display:block;color:#687684;font-size:12px;margin-top:3px}.status{display:flex;align-items:center;gap:8px;padding:8px 12px;border:1px solid #dce3e8;border-radius:999px;background:#fff;color:#53616e;font-size:12px}.dot{width:8px;height:8px;border-radius:50%;background:#29905b}
.hero{text-align:center;padding:24px 12px 20px}.eyebrow{color:#0b6e69;text-transform:uppercase;letter-spacing:.14em;font-size:11px;font-weight:800}.hero h1{font-size:clamp(28px,4.5vw,44px);line-height:1.12;letter-spacing:-.04em;margin:12px auto 10px;max-width:760px}.hero p{color:#5b6977;margin:0 auto;max-width:620px;line-height:1.55;font-size:15px}
.workspace{display:grid;grid-template-columns:minmax(0,1fr) 250px;gap:18px;align-items:stretch}.chat{min-height:500px;background:#fff;border:1px solid #e1e7eb;border-radius:20px;box-shadow:0 16px 45px #20333e0c;display:flex;flex-direction:column;overflow:hidden}.chat-head{display:flex;align-items:center;justify-content:space-between;padding:15px 18px;border-bottom:1px solid #edf0f2}.chat-title{font-size:13px;font-weight:750}.fresh{border:0;background:transparent;color:#0b6e69;font:inherit;font-size:12px;font-weight:700;cursor:pointer;padding:7px 9px;border-radius:8px}.fresh:hover{background:#edf7f5}
.messages{flex:1;min-height:340px;max-height:510px;overflow:auto;padding:20px;display:flex;flex-direction:column;gap:14px}.msg{max-width:min(88%,690px);padding:12px 15px;border-radius:15px;font-size:14px;line-height:1.55;white-space:pre-wrap;overflow-wrap:anywhere}.msg.bot{align-self:flex-start;background:#f1f5f5;border:1px solid #e7eeee;border-top-left-radius:5px}.msg.user{align-self:flex-end;background:#0b6e69;color:#fff;border-top-right-radius:5px}.msg.error{background:#fff4e7;border-color:#f2dfc4;color:#754e17}.meta{display:block;color:#7c8a96;font-size:10px;margin-top:8px}.user .meta{color:#d0e8e5}.typing{color:#73818d;font-size:12px;padding:0 20px 10px;display:none}
.composer{border-top:1px solid #edf0f2;padding:14px 16px 12px}.compose-row{display:flex;align-items:flex-end;gap:10px;padding:8px 8px 8px 14px;border:1px solid #dce3e8;border-radius:15px;background:#fff;transition:border-color .15s,box-shadow .15s}.compose-row:focus-within{border-color:#75aaa4;box-shadow:0 0 0 3px #0b6e6910}textarea{flex:1;min-height:42px;max-height:130px;resize:vertical;border:0;outline:0;font:inherit;font-size:14px;line-height:1.5;color:#17212b;padding:9px 0;background:transparent}textarea::placeholder{color:#98a3ac}.send{width:42px;height:42px;border:0;border-radius:12px;background:#0b6e69;color:white;font-size:19px;font-weight:700;cursor:pointer}.send:disabled{opacity:.5;cursor:wait}.hint{display:flex;justify-content:space-between;gap:12px;color:#87939d;font-size:10px;padding:9px 3px 0}
.side{display:flex;flex-direction:column;gap:14px}.card{background:#fff;border:1px solid #e1e7eb;border-radius:17px;padding:17px;box-shadow:0 12px 32px #20333e08}.card h2{font-size:13px;margin:0 0 12px}.card p{font-size:12px;line-height:1.55;color:#687684;margin:0}.examples{display:grid;gap:8px}.example{width:100%;text-align:left;border:1px solid #e2e8eb;border-radius:11px;background:#fff;padding:10px 11px;color:#36434e;font:inherit;font-size:11px;line-height:1.4;cursor:pointer}.example:hover{border-color:#9fc6c2;background:#f7fbfa}.guard{display:grid;gap:10px}.guard-line{display:flex;gap:9px;color:#586773;font-size:11px;line-height:1.4}.check{flex:0 0 18px;width:18px;height:18px;display:grid;place-items:center;background:#eaf5f2;color:#0b6e69;border-radius:6px;font-weight:800}.notice{margin-top:auto;background:#fff9eb;border:1px solid #f0e5c6;border-radius:13px;padding:12px;color:#725b27;font-size:11px;line-height:1.45}
.footer{text-align:center;color:#9aa4ac;font-size:10px;padding:18px 0 0}
@media(max-width:760px){.shell{padding:16px 12px 24px}.top{margin-bottom:8px}.workspace{grid-template-columns:1fr}.chat{min-height:470px}.side{display:grid;grid-template-columns:1fr 1fr}.notice{grid-column:1/-1}.hero{padding:25px 8px 19px}.messages{padding:15px;max-height:55vh}}
@media(max-width:480px){.brand span{display:none}.status{font-size:10px;padding:7px 9px}.side{grid-template-columns:1fr}.notice{grid-column:auto}.msg{max-width:94%}}
</style>
</head>
<body>
<main class="shell">
  <header class="top">
    <div class="brand"><div class="logo">H</div><div><strong>HappyWindBoys</strong><span>Trợ giảng mini lab · Track A</span></div></div>
    <div class="status"><span class="dot"></span><span id="model-status">Đang kết nối…</span></div>
  </header>
  <section class="hero">
    <div class="eyebrow">Cùng bạn tự hoàn thành lab</div>
    <h1>Kẹt ở bước nào?<br>Hãy bắt đầu từ đó.</h1>
    <p>Mô tả lab, bước hiện tại và điều bạn đã thử. Trợ giảng sẽ đưa gợi ý có căn cứ hoặc hỏi thêm khi chưa đủ thông tin.</p>
  </section>
  <section class="workspace">
    <section class="chat" aria-label="Trò chuyện với trợ giảng">
      <div class="chat-head"><div class="chat-title">Cuộc trò chuyện</div><button class="fresh" id="clear">Cuộc trò chuyện mới</button></div>
      <div class="messages" id="messages" aria-live="polite">
        <div class="msg bot">Chào bạn! Mình có thể gợi ý từng bước dựa trên đề lab được cung cấp. Hãy cho mình biết mã lab, bạn đang ở bước nào và đã thử cách gì nhé.<span class="meta">Trợ giảng mini lab · luôn kiểm tra lại gợi ý với đề bài</span></div>
      </div>
      <div class="typing" id="typing">Đang xem thông tin lab…</div>
      <form class="composer" id="form">
        <div class="compose-row"><textarea id="prompt" rows="1" maxlength="3000" placeholder="Ví dụ: Mình đang làm lab d01-lab-ban-la-llm, bước 1. Mình đã thử…" aria-label="Tin nhắn của bạn"></textarea><button class="send" id="send" type="submit" aria-label="Gửi">↑</button></div>
        <div class="hint"><span>Enter để gửi · Shift+Enter xuống dòng</span><span id="counter">0/3000</span></div>
      </form>
    </section>
    <aside class="side">
      <section class="card"><h2>Thử một câu</h2><div class="examples">
        <button class="example" data-text="Mình mở lab d01-lab-ban-la-llm nhưng chưa hoàn thành. Mình không biết tiếp tục thế nào.">Mình chưa hoàn thành lab, nên tiếp tục thế nào?</button>
        <button class="example" data-text="Mình đang làm lab d01-lab-ban-la-llm, đã hoàn thành bước 1/2. Hãy gợi ý bước tiếp theo.">Mình đã xong bước 1/2, gợi ý bước tiếp theo</button>
        <button class="example" data-text="Bạn có thể làm và nộp toàn bộ mini lab thay mình không?">Xin làm hộ toàn bộ lab</button>
      </div></section>
      <section class="card"><h2>Nguyên tắc hỗ trợ</h2><div class="guard">
        <div class="guard-line"><span class="check">✓</span><span>Gợi ý dựa trên thông tin lab đã có</span></div>
        <div class="guard-line"><span class="check">✓</span><span>Hỏi lại khi chưa rõ bước hoặc chỗ kẹt</span></div>
        <div class="guard-line"><span class="check">✓</span><span>Không làm bài hoặc cung cấp đáp án thay bạn</span></div>
      </div></section>
      <div class="notice">Bản demo dùng dữ liệu minh họa. Hãy đối chiếu gợi ý với đề bài; nếu kẹt quá 15 phút, hỏi lab coach.</div>
    </aside>
  </section>
  <div class="footer">Mỗi tin nhắn được xử lý độc lập · bản demo không lưu lịch sử trò chuyện</div>
</main>
<script>
const form=document.getElementById('form'), promptBox=document.getElementById('prompt'), messages=document.getElementById('messages'), send=document.getElementById('send'), typing=document.getElementById('typing'), counter=document.getElementById('counter');
function addMessage(text,who,meta='',error=false){const node=document.createElement('div');node.className='msg '+who+(error?' error':'');node.textContent=text;if(meta){const small=document.createElement('span');small.className='meta';small.textContent=meta;node.appendChild(small)}messages.appendChild(node);messages.scrollTop=messages.scrollHeight;return node}
function cleanReply(output){
  const disclaimer='Gợi ý do AI tạo, có thể chưa đúng. Kẹt quá 15 phút thì hỏi lab coach.';
  const lines=String(output||'').split(/\r?\n/).map(line=>line.trim()).filter(Boolean);
  if(lines.length&&/^\[GỢI Ý\]/i.test(lines[0]))lines.shift();
  else if(lines.length)lines[0]=lines[0].replace(/^\[(?:HỎI LẠI|TỪ CHỐI)\]\s*/i,'');
  return lines.filter(line=>line!==disclaimer&&!/^Căn cứ\s*:/i.test(line)).join('\n').trim()||'Mình chưa có nội dung trả lời.';
}
form.addEventListener('submit',async event=>{event.preventDefault();const message=promptBox.value.trim();if(!message||send.disabled)return;addMessage(message,'user');promptBox.value='';counter.textContent='0/3000';send.disabled=true;typing.style.display='block';try{const response=await fetch('/api/chat',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({message})});const data=await response.json();if(!response.ok)throw new Error(data.error||'Không gửi được tin nhắn.');addMessage(cleanReply(data.output),'bot')}catch(error){addMessage(error.message||'Có lỗi kết nối. Hãy thử lại.','bot','',true)}finally{typing.style.display='none';send.disabled=false;promptBox.focus()}});
promptBox.addEventListener('input',()=>counter.textContent=promptBox.value.length+'/3000');
promptBox.addEventListener('keydown',event=>{if(event.key==='Enter'&&!event.shiftKey){event.preventDefault();form.requestSubmit()}});
document.querySelectorAll('.example').forEach(button=>button.addEventListener('click',()=>{promptBox.value=button.dataset.text;counter.textContent=promptBox.value.length+'/3000';promptBox.focus()}));
document.getElementById('clear').addEventListener('click',()=>{messages.replaceChildren();addMessage('Chào bạn! Mình có thể gợi ý từng bước dựa trên đề lab được cung cấp. Hãy cho mình biết mã lab, bạn đang ở bước nào và đã thử cách gì nhé.','bot','Trợ giảng mini lab · luôn kiểm tra lại gợi ý với đề bài');promptBox.focus()});
fetch('/api/status').then(r=>r.json()).then(data=>{document.getElementById('model-status').textContent=data.label}).catch(()=>{document.getElementById('model-status').textContent='Sẵn sàng demo'});
</script>
</body>
</html>"""


def _json_response(handler, status, payload):
    body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
    handler.send_response(status)
    handler.send_header("Content-Type", "application/json; charset=utf-8")
    handler.send_header("Content-Length", str(len(body)))
    handler.send_header("Cache-Control", "no-store")
    handler.send_header("X-Content-Type-Options", "nosniff")
    handler.end_headers()
    handler.wfile.write(body)


def _friendly_error(exc):
    """Map backend failures to useful hints without returning raw API details."""
    detail = str(exc).casefold()
    if "timeout" in detail or "timed out" in detail:
        return "Gemini chưa phản hồi đúng hạn; hệ thống đã thử lại một lần. Hãy chờ ít phút rồi gửi lại."
    if "429" in detail or "quota" in detail or "rate limit" in detail:
        return "Gemini đang giới hạn lượt gọi. Chờ một chút rồi thử lại."
    if "401" in detail or "403" in detail or "api_key" in detail or "api key" in detail:
        return "Gemini từ chối xác thực. Kiểm tra API_KEY và quyền truy cập trong file .env."
    if "không kết nối" in detail or "urlerror" in detail or "network" in detail:
        return "Không kết nối được Gemini. Kiểm tra mạng rồi thử lại."
    if "404" in detail or "model" in detail and "not found" in detail:
        return "Không tìm thấy model Gemini đã cấu hình. Kiểm tra MODEL_NAME trong file .env."
    return "Trợ giảng gặp lỗi khi tạo câu trả lời. Xem cửa sổ lệnh chạy python run.py để biết chi tiết."


class DemoHandler(BaseHTTPRequestHandler):
    server_version = "HappyWindDemo/1.0"

    def log_message(self, fmt, *args):
        print("[web] " + fmt % args)

    def do_GET(self):
        if self.path == "/" or self.path == "/index.html":
            body = PAGE.encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.send_header("Cache-Control", "no-store")
            self.send_header("X-Content-Type-Options", "nosniff")
            self.end_headers()
            self.wfile.write(body)
            return
        if self.path == "/api/status":
            if ai.MODEL_PROVIDER == "gemini":
                label = "Gemini · " + (ai.MODEL_NAME or "đã chọn model")
            else:
                label = "Chế độ demo ngoại tuyến"
            _json_response(self, 200, {"label": label})
            return
        _json_response(self, 404, {"error": "Không tìm thấy trang."})

    def do_POST(self):
        if self.path != "/api/chat":
            _json_response(self, 404, {"error": "Không tìm thấy đường dẫn."})
            return
        try:
            length = int(self.headers.get("Content-Length", "0"))
        except ValueError:
            _json_response(self, 400, {"error": "Yêu cầu không hợp lệ."})
            return
        if length <= 0 or length > MAX_BODY:
            _json_response(self, 413, {"error": "Tin nhắn trống hoặc vượt quá giới hạn."})
            return
        try:
            payload = json.loads(self.rfile.read(length).decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError):
            _json_response(self, 400, {"error": "Không đọc được nội dung gửi lên."})
            return
        message = payload.get("message") if isinstance(payload, dict) else None
        if not isinstance(message, str) or not message.strip() or len(message) > 3000:
            _json_response(self, 400, {"error": "Hãy nhập tin nhắn từ 1 đến 3000 ký tự."})
            return

        tracing.begin("web-demo")
        try:
            result = answer(message.strip())
            usage, _ = tracing.end()
        except Exception as exc:
            tracing.end()
            print("[lỗi trợ giảng] %s: %s" % (type(exc).__name__, exc))
            _json_response(self, 502, {"error": _friendly_error(exc)})
            return
        output = result.get("output", "") if isinstance(result, dict) else str(result)
        _json_response(self, 200, {"output": output, "usage": usage})


def main() -> int:
    try:
        server = HTTPServer((HOST, PORT), DemoHandler)
    except OSError as exc:
        print("Không mở được giao diện tại http://%s:%d (%s). Hãy kiểm tra cổng %d." % (HOST, PORT, exc, PORT))
        return 1
    url = "http://%s:%d" % (HOST, PORT)
    print("Giao diện demo đang chạy tại %s · nhấn Ctrl+C để thoát." % url)
    try:
        webbrowser.open(url)
    except Exception:
        pass
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nĐã dừng giao diện demo.")
    finally:
        server.server_close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
