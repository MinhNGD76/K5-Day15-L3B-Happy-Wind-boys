"""Đếm bằng chứng pain từ data pre-class (chạy lại: python evidence/count.py).

Data BTC để ở data-btc/preclass/ (gitignore, không commit). Script chỉ in số tổng hợp.
"""
import csv
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")  # console Windows mặc định cp1252, không in được tiếng Việt
DATA = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).resolve().parent.parent / "data-btc" / "preclass"


def rows(name):
    with open(DATA / name, encoding="utf-8-sig", newline="") as f:
        yield from csv.DictReader(f)


def data(r):
    return json.loads(r["data"] or "{}")


def pct(x, n):
    return f"{x}/{n} ({100 * x / n:.1f}%)" if n else f"{x}/0"


events = [r for r in rows("events.csv") if r["type"] in ("lab_opened", "lab_completed", "agent_replied")]
active = {r["hv"] for r in rows("events.csv")}
chat = {r["id"]: r for r in rows("chat.csv")}

# --- 1. Mini lab: một cặp (học viên, lab_key) đã mở lab, kết cục ra sao ---
opened = {}            # (hv, lab_key) -> ngày mở đầu tiên
real_done = set()      # có ít nhất 1 lab_completed với skipped != True
skipped = {}           # (hv, lab_key) -> (steps_done, steps) của lần bỏ qua cuối
for r in events:
    if r["type"] == "lab_opened":
        opened.setdefault((r["hv"], data(r).get("lab_key")), r["occurred_at"][:10])
    elif r["type"] == "lab_completed":
        x = data(r)
        k = (r["hv"], x.get("lab_key"))
        if x.get("skipped") is True:
            skipped[k] = (x.get("steps_done"), x.get("steps"))
        else:
            real_done.add(k)

n = len(opened)
done = sum(k in real_done for k in opened)
only_skip = sum(k not in real_done and k in skipped for k in opened)
never = sum(k not in real_done and k not in skipped for k in opened)
assert done + only_skip + never == n, "ba nhóm kết cục phải cộng đủ mẫu số"

print("== 1. Mini lab (mẫu số: cặp học viên × lab đã mở) ==")
print("Học viên hoạt động:", len(active), "· học viên mở ≥1 lab:", len({k[0] for k in opened}))
print("Cặp học viên × lab đã mở:", n)
print("  Làm xong thật      :", pct(done, n))
print("  Chỉ bấm bỏ qua     :", pct(only_skip, n))
print("  Bỏ dở, không kết   :", pct(never, n))
print("  => Không làm xong  :", pct(only_skip + never, n))

stuck = Counter(hv for hv, lab in opened if (hv, lab) not in real_done)
print("Học viên có ≥1 lab không làm xong:", pct(len(stuck), len({k[0] for k in opened})))

print("Bỏ qua ở bước nào (steps_done/steps):", Counter(f"{a}/{b}" for a, b in
      (skipped[k] for k in opened if k not in real_done and k in skipped)).most_common(6))

per_lab = defaultdict(lambda: [0, 0])
for k in opened:
    per_lab[k[1]][0] += 1
    per_lab[k[1]][1] += k not in real_done
print("Lab mở nhiều nhất (không xong / số cặp đã mở):")
for lab, (o, s) in sorted(per_lab.items(), key=lambda kv: -kv[1][0])[:6]:
    print(f"  {lab}: {pct(s, o)}")

# --- 2. Trợ giảng dưới video (để so hướng, bảng impact) ---
vq = [data(r) for r in events if r["type"] == "agent_replied"
      and chat.get(r["ref_id"], {}).get("channel") == "video_question"]
logged = [x for x in vq if "moc_trich_dan" in x]  # trường này chỉ có từ 13/11
print("\n== 2. Trợ giảng dưới video ==")
print("Học viên có bản ghi chat (mọi kênh):", pct(len({c["hv"] for c in chat.values()}), len(active)))
print("Trả lời thiếu ngữ cảnh (missing_context):", pct(sum(x.get("missing_context") is True for x in vq), len(vq)))
print("Trả lời không trích mốc giây (chỉ dòng có ghi trường, từ 13/11):",
      pct(sum(not x["moc_trich_dan"] for x in logged), len(logged)))
