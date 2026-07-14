# -*- coding: utf-8 -*-
"""変換前(contacts.csv)→変換後(編集用マスター)の対比レポートをMarkdown出力。"""
import csv
from collections import Counter

SRC = r"C:\Users\bwd001.BWD\OneDrive - bwd group\ドキュメント\Claude oguro\oguro-private\project\連絡先\contacts.csv"
DST = r"C:\Users\bwd001.BWD\OneDrive - bwd group\ドキュメント\Claude oguro\oguro-private\project\連絡先\連絡先_編集用マスター.csv"
OUT = r"C:\Users\bwd001.BWD\AppData\Local\Temp\claude\c--Users-bwd001-BWD-OneDrive---bwd-group--------Claude-oguro-oguro-private\2994732c-900c-440f-93b9-79068720ad58\scratchpad\変換確認.md"

with open(SRC, encoding="utf-8-sig") as f:
    src = list(csv.DictReader(f))
with open(DST, encoding="utf-8-sig") as f:
    dst = list(csv.DictReader(f))

o=[]
o.append("# 変換前→変換後 対比レポート\n")
o.append("## サンプル20件（Before → After）\n")
for i in range(20):
    s, d = src[i], dst[i]
    o.append(f"### {i+1}")
    o.append(f"- **Before**: 名={s.get('First Name','')} / ミドル={s.get('Middle Name','')} / 姓={s.get('Last Name','')} / 敬称={s.get('Name Suffix','')}")
    o.append(f"- **After** : 姓=**{d['姓']}** 名=**{d['名']}** ﾌﾘｶﾞﾅ={d['姓フリガナ']} 会社=**{d['会社名']}** 役職={d['役職']}")
    if d['要確認']:
        o.append(f"  - ⚠ 要確認: {d['要確認']}")
    o.append("")

o.append("## 要確認フラグ内訳\n")
c=Counter(r['要確認'] for r in dst if r['要確認'])
for k,v in c.most_common():
    o.append(f"- {v:>4}  {k}")

o.append("\n## 肩書きを分離できた30件\n```")
for r in dst:
    if r['役職']:
        o.append(f"姓={r['姓']}  役職={r['役職']}  会社={r['会社名']}")
o.append("```")

# 空白ありで姓名分割できた例
o.append("\n## 姓名分割に成功した例（空白ありデータ・先頭20）\n```")
cnt=0
for r in dst:
    if r['名'] and not r['要確認']:
        o.append(f"姓={r['姓']}  名={r['名']}  ﾌﾘｶﾞﾅ={r['姓フリガナ']}  会社={r['会社名']}")
        cnt+=1
        if cnt>=20: break
o.append("```")

with open(OUT,"w",encoding="utf-8") as f:
    f.write("\n".join(o))
print("wrote",OUT)
