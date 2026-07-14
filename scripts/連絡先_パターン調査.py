# -*- coding: utf-8 -*-
"""正規化の前に、氏名分割・肩書き・会社名のパターンを調査する。"""
import csv, re
from collections import Counter

SRC = r"C:\Users\bwd001.BWD\OneDrive - bwd group\ドキュメント\Claude oguro\oguro-private\project\連絡先\contacts.csv"
OUT = r"C:\Users\bwd001.BWD\AppData\Local\Temp\claude\c--Users-bwd001-BWD-OneDrive---bwd-group--------Claude-oguro-oguro-private\2994732c-900c-440f-93b9-79068720ad58\scratchpad\パターン調査.md"

with open(SRC, encoding="utf-8-sig", newline="") as f:
    rows = list(csv.DictReader(f))

TITLES = ["代表取締役","取締役","代表","会長","副社長","社長","専務","常務","本部長","事業部長",
          "部長代理","課長代理","次長","部長","課長","係長","主任","主査","主幹","室長","所長",
          "支店長","店長","工場長","統括","顧問","相談役","秘書","マネージャー","リーダー","担当","専任"]

def g(r,k): return (r.get(k) or "").strip()

n_space = n_nospace = n_title = n_empty_kanji = 0
title_counter = Counter()
no_space_examples = []
title_examples = []
company_in_notes = 0

for r in rows:
    kanji = g(r,"Middle Name")
    company = g(r,"Last Name")
    notes = g(r,"Notes")
    if not kanji:
        n_empty_kanji += 1
        continue
    # 肩書き検出
    found_title = None
    for t in TITLES:
        if t in kanji:
            found_title = t
            break
    if found_title:
        n_title += 1
        title_counter[found_title]+=1
        if len(title_examples)<25:
            title_examples.append(f"{kanji}  →(社名:{company})")
    # 空白有無
    if re.search(r"[\s　]", kanji):
        n_space += 1
    else:
        n_nospace += 1
        if len(no_space_examples)<40:
            no_space_examples.append(f"{kanji}  (ローマ字:{g(r,'First Name')} / 社名:{company})")

out=[]
out.append("# 正規化パターン調査\n")
out.append(f"- 総件数: {len(rows)}")
out.append(f"- 漢字氏名(Middle Name)が空: {n_empty_kanji}")
out.append(f"- 漢字氏名に空白あり(姓名分割しやすい): {n_space}")
out.append(f"- 漢字氏名に空白なし(分割に判断必要): {n_nospace}")
out.append(f"- 肩書きらしき語を含む: {n_title}")
out.append("\n## 検出された肩書き語の内訳\n")
for t,c in title_counter.most_common():
    out.append(f"- {c:>4}  {t}")
out.append("\n## 肩書きを含む氏名の例\n```")
out += title_examples
out.append("```")
out.append("\n## 空白なし漢字氏名の例（姓名分割の判断が要る）\n```")
out += no_space_examples
out.append("```")

# 会社名(Last Name)のユニーク値の一部と件数
comp = Counter(g(r,"Last Name") for r in rows if g(r,"Last Name"))
out.append(f"\n## 企業名(現・姓欄) ユニーク数: {len(comp)}\n")
out.append("### 多い企業トップ30\n```")
for name,c in comp.most_common(30):
    out.append(f"{c:>4}  {name}")
out.append("```")

with open(OUT,"w",encoding="utf-8") as f:
    f.write("\n".join(out))
print("wrote", OUT)
