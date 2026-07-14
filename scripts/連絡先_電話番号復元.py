# -*- coding: utf-8 -*-
"""Excelで先頭0が脱落した電話番号を、元データ(contacts.csv)から復元する。
No列で元データと突き合わせ、「0落ち」パターンのセルだけをピンポイント復元する
（ユーザーの手直しは温存）。"""
import csv, re

MASTER = r"C:\Users\bwd001.BWD\OneDrive - bwd group\ドキュメント\Claude oguro\oguro-private\project\連絡先\連絡先_編集用マスター.csv"
ORIG   = r"C:\Users\bwd001.BWD\OneDrive - bwd group\ドキュメント\Claude oguro\oguro-private\project\連絡先\contacts.csv"

# 元データ: No(=1始まりの行番号) → 元の電話値
with open(ORIG, encoding="utf-8-sig", newline="") as f:
    orig = list(csv.DictReader(f))
orig_phone = {}  # No -> {電話1, 電話2}
for i, r in enumerate(orig, 1):
    orig_phone[str(i)] = {
        "電話1": (r.get("Phone 1 - Value") or "").strip(),
        "電話2": (r.get("Phone 2 - Value") or "").strip(),
    }

def digits(s): return re.sub(r"[^0-9]", "", s or "")

def is_zero_dropped(cur, orig_val):
    """curが「orig_valの先頭0を落とした値」と一致するか判定。"""
    dc, do = digits(cur), digits(orig_val)
    if not dc or not do:
        return False
    # 元が0始まりで、現在が0を除いたものと一致 → 0落ち
    return do.startswith("0") and dc == do.lstrip("0") and dc != do

with open(MASTER, encoding="utf-8-sig", newline="") as f:
    reader = csv.DictReader(f)
    fields = reader.fieldnames
    rows = list(reader)

fixed = []
for r in rows:
    no = r.get("No")
    if no not in orig_phone:
        continue
    for col in ("電話1", "電話2"):
        cur = r.get(col, "")
        ov  = orig_phone[no][col]
        if is_zero_dropped(cur, ov):
            r[col] = ov
            fixed.append(f"No.{no} {col}: {cur} → {ov}")

with open(MASTER, "w", encoding="utf-8-sig", newline="") as f:
    w = csv.DictWriter(f, fieldnames=fields)
    w.writeheader()
    w.writerows(rows)

print(f"復元件数: {len(fixed)}")
for line in fixed:
    print(" ", line)
