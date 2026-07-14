# -*- coding: utf-8 -*-
"""Google連絡先CSVの中身を分析し、Markdownレポートを出力する。"""
import csv

CSV_PATH = r"C:\Users\bwd001.BWD\OneDrive - bwd group\ドキュメント\Claude oguro\oguro-private\project\連絡先\contacts.csv"
OUT_PATH = r"C:\Users\bwd001.BWD\AppData\Local\Temp\claude\c--Users-bwd001-BWD-OneDrive---bwd-group--------Claude-oguro-oguro-private\2994732c-900c-440f-93b9-79068720ad58\scratchpad\連絡先レポート.md"

with open(CSV_PATH, encoding="utf-8-sig", newline="") as f:
    reader = csv.DictReader(f)
    rows = list(reader)
    fields = reader.fieldnames

total = len(rows)
out = []
out.append(f"# 連絡先CSV分析レポート\n\n総件数: {total}\n")

out.append("## 使われている列（空でない件数）\n")
for col in fields:
    n = sum(1 for r in rows if (r.get(col) or "").strip())
    if n > 0:
        out.append(f"- {n:>5} / {total}  `{col}`")

# 注目カラムのサンプル
key_cols = ["First Name", "Middle Name", "Last Name",
            "Phonetic Last Name", "Phonetic First Name",
            "Nickname", "Name Suffix", "File As",
            "Organization Name", "Organization Title",
            "Notes", "Labels",
            "E-mail 1 - Value", "Phone 1 - Value", "Phone 1 - Label"]
key_cols = [c for c in key_cols if c in fields]

out.append("\n## 主要カラムのサンプル（先頭30件）\n")
for i, r in enumerate(rows[:30]):
    out.append(f"\n### {i+1}")
    for c in key_cols:
        v = (r.get(c) or "").strip()
        if v:
            out.append(f"- **{c}**: {v}")

# Middle Name / Nickname / Name Suffix の値パターンを見る
for target in ["Middle Name", "Nickname", "Name Suffix", "Phone 1 - Label"]:
    vals = [(r.get(target) or "").strip() for r in rows]
    vals = [v for v in vals if v]
    out.append(f"\n## `{target}` の値サンプル（最初の40個）\n")
    out.append("```")
    for v in vals[:40]:
        out.append(v)
    out.append("```")

# Labels（グループ）の集計
from collections import Counter
label_counter = Counter()
for r in rows:
    labs = (r.get("Labels") or "").strip()
    for lab in labs.split(" ::: "):
        lab = lab.strip()
        if lab:
            label_counter[lab] += 1
out.append("\n## Labels（グループ）の集計\n")
for lab, n in label_counter.most_common():
    out.append(f"- {n:>4}  {lab}")

with open(OUT_PATH, "w", encoding="utf-8") as f:
    f.write("\n".join(out))

print("wrote:", OUT_PATH)
