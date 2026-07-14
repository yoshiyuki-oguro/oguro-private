# -*- coding: utf-8 -*-
"""会社名の大文字小文字の表記ゆれを、最頻出の表記に統一する（マスターを上書き）。
別綴り(タイプミス)は自動統合せず、別途レポートするだけに留める。"""
import csv
from collections import Counter, defaultdict

MASTER = r"C:\Users\bwd001.BWD\OneDrive - bwd group\ドキュメント\Claude oguro\oguro-private\project\連絡先\連絡先_編集用マスター.csv"

with open(MASTER, encoding="utf-8-sig", newline="") as f:
    reader = csv.DictReader(f)
    fields = reader.fieldnames
    rows = list(reader)

comp = Counter(r["会社名"].strip() for r in rows if r["会社名"].strip())

# casefold(大小無視)でグループ化し、代表表記を決める
groups = defaultdict(list)
for name, c in comp.items():
    groups[name.casefold()].append((name, c))

def canonical(variants):
    """代表表記: 出現数最多。同数なら「全大文字/全小文字でない(Title/Mixed)」を優先。"""
    def rank(item):
        name, c = item
        mixed = 0 if (name.isupper() or name.islower()) else 1
        return (c, mixed)
    return max(variants, key=rank)[0]

canon_map = {}
for k, v in groups.items():
    if len(v) > 1:
        cn = canonical(v)
        for name, _ in v:
            if name != cn:
                canon_map[name] = cn

# 適用
changed = 0
for r in rows:
    c = r["会社名"].strip()
    if c in canon_map:
        r["会社名"] = canon_map[c]
        changed += 1

with open(MASTER, "w", encoding="utf-8-sig", newline="") as f:
    w = csv.DictWriter(f, fieldnames=fields)
    w.writeheader()
    w.writerows(rows)

print("統一ルール:")
for src, dst in sorted(canon_map.items()):
    print(f"  {src} → {dst}")
print(f"変更レコード数: {changed}")
