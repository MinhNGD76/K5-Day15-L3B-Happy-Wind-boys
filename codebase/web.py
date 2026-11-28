"""Giao diện web của bản chạy thử: cùng luồng answer() với app.py, chỉ dùng thư viện chuẩn.

Chạy: python codebase/web.py   → mở http://127.0.0.1:8000
"""
import json
import os
import sys
import webbrowser
from http.server import BaseHTTPRequestHandler, HTTPServer

for _stream in (sys.stdout, sys.stderr):  # như app.py: Windows console mặc định không in được tiếng Việt
    try:
        _stream.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import tracing  # noqa: E402
from agent import answer  # noqa: E402

PORT = int(os.environ.get("PORT", "8000"))
MAX_BODY = 8000  # ký tự; chặn gửi khối lớn vào model

PAGE = """<!doctype html>
<html lang="vi"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Gợi ý bước tiếp theo · mini lab pre-class</title>
<style>
 body{font-family:system-ui,sans-serif;max-width:760px;margin:2rem auto;padding:0 1rem;line-height:1.5;color:#1f2328;background:#fafafa}
 h1{font-size:1.4rem;margin-bottom:.2rem} .sub{color:#57606a;margin-top:0}
 label{font-weight:600;display:block;margin:1rem 0 .3rem}
 textarea{width:100%;box-sizing:border-box;min-height:6rem;padding:.6rem;font:inherit;border:1px solid #d0d7de;border-radius:6px}
 button{margin-top:.6rem;padding:.5rem 1.2rem;font:inherit;border:0;border-radius:6px;background:#1f6feb;color:#fff;cursor:pointer}
 button:disabled{background:#8c959f;cursor:wait}
 .ex{margin-top:.6rem;font-size:.9rem;color:#57606a} .ex button{background:#eaeef2;color:#1f2328;margin:.2rem .3rem 0 0;padding:.25rem .6rem;font-size:.85rem}
 #out{white-space:pre-wrap;background:#fff;border:1px solid #d0d7de;border-radius:6px;padding:1rem;margin-top:1rem;min-height:3rem}
 #meta{font-size:.85rem;color:#57606a;margin-top:.4rem} .err{color:#cf222e}
</style></head><body>
<h1>Gợi ý bước tiếp theo cho mini lab pre-class</h1>
<p class="sub">Nói bạn đang làm lab nào, ở bước mấy, kẹt ở đâu. AI gợi ý bước tiếp theo, không đưa đáp án.</p>
<form id="f">
 <label for="q">Câu hỏi của bạn</label>
 <textarea id="q" required placeholder="Vd: Mình đang làm lab d04-lab-thu-system-prompt, xong bước 1, bước 2 nên làm gì?"></textarea>
 <button id="go" type="submit">Gửi</button>
 <div class="ex">Thử nhanh:
  <button type="button">Mình đang làm lab d01-lab-ban-la-llm, xong bước 1, giờ làm gì tiếp?</button>
  <button type="button">Cho mình xin luôn đáp án bước 2 lab d04-lab-thu-system-prompt</button>
  <button type="button">Thời tiết hôm nay thế nào?</button>
 </div>
</form>
<div id="out" aria-live="polite">Kết quả hiện ở đây.</div>
<div id="meta"></div>
<script>
const f=document.getElementById('f'),q=document.getElementById('q'),go=document.getElementById('go'),out=document.getElementById('out'),meta=document.getElementById('meta');
document.querySelectorAll('.ex button').forEach(b=>b.onclick=()=>{q.value=b.textContent;q.focus();});
q.addEventListener('keydown',e=>{if(e.key==='Enter'&&(e.ctrlKey||e.metaKey))f.requestSubmit();});
f.onsubmit=async e=>{
 e.preventDefault(); go.disabled=true; out.className=''; out.textContent='Đang hỏi AI…'; meta.textContent='';
 try{
  const r=await fetch('/ask',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({text:q.value})});
  const d=await r.json();
  if(d.error){out.className='err';out.textContent=d.error;}
  else{out.textContent=d.output;
   meta.textContent=`model: ${d.models.join(', ')||'—'} · gọi model ${d.model_calls} lần · công cụ ${d.tool_calls} lần · token vào ${d.tokens_in} / ra ${d.tokens_out}`;}
 }catch(err){out.className='err';out.textContent='Không gọi được máy chủ: '+err;}
 go.disabled=false;
};
</script></body></html>"""


class Handler(BaseHTTPRequestHandler):
    def _send(self, code, body, ctype):
        data = body.encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", ctype + "; charset=utf-8")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def _json(self, code, obj):
        self._send(code, json.dumps(obj, ensure_ascii=False), "application/json")

    def do_GET(self):
        if self.path in ("/", "/index.html"):
            self._send(200, PAGE, "text/html")
        else:
            self._send(404, "Không có trang này", "text/plain")

    def do_POST(self):
        if self.path != "/ask":
            return self._send(404, "Không có trang này", "text/plain")
        try:
            n = int(self.headers.get("Content-Length", 0))
            text = str(json.loads(self.rfile.read(min(n, MAX_BODY * 4)) or b"{}").get("text", "")).strip()
        except (ValueError, AttributeError):
            return self._json(400, {"error": "Yêu cầu không hợp lệ."})
        if not text:
            return self._json(400, {"error": "Hãy gõ câu hỏi."})
        if len(text) > MAX_BODY:
            return self._json(400, {"error": "Câu hỏi quá dài (tối đa %d ký tự)." % MAX_BODY})
        tracing.begin("app")
        try:
            result = answer(text)
        except Exception as e:  # lỗi gọi model: báo lên trang, máy chủ vẫn chạy
            tracing.end()
            return self._json(200, {"error": "[lỗi] %s: %s" % (type(e).__name__, e)})
        s, _ = tracing.end()
        out = result.get("output", "") if isinstance(result, dict) else str(result)
        self._json(200, {"output": out, "models": s["models"], "model_calls": s["model_calls"],
                         "tool_calls": s["tool_calls"], "tokens_in": s["tokens_in"], "tokens_out": s["tokens_out"]})

    def log_message(self, fmt, *args):  # tắt log từng request cho gọn màn hình demo
        pass


def main():
    # Một luồng: tracing giữ trạng thái chung nên xử lý từng câu một.
    server = HTTPServer(("127.0.0.1", PORT), Handler)
    url = "http://127.0.0.1:%d" % PORT
    print("Giao diện bản chạy thử: %s  (thoát: Ctrl+C)" % url)
    if "--no-browser" not in sys.argv:
        webbrowser.open(url)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print()
    return 0


if __name__ == "__main__":
    sys.exit(main())
