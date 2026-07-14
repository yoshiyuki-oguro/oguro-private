# -*- coding: utf-8 -*-
"""Google連絡先CSV(UTF-8)を、Excelで文字化けせず開けるBOM付きCSVに変換。
使っている主要列だけに絞り、日本語見出しにして確認しやすくする。"""
import csv

SRC = r"C:\Users\bwd001.BWD\OneDrive - bwd group\ドキュメント\Claude oguro\oguro-private\project\連絡先\contacts.csv"
DST = r"C:\Users\bwd001.BWD\OneDrive - bwd group\ドキュメント\Claude oguro\oguro-private\project\連絡先\連絡先_確認用.csv"

# 元の列名 → 日本語見出し（使っている列＝分析で1件以上あったもの中心）
COLMAP = [
    ("First Name", "名(ローマ字)"),
    ("Middle Name", "氏名(漢字)"),
    ("Last Name", "企業名(現:姓欄)"),
    ("Phonetic Last Name", "姓フリガナ欄"),
    ("Phonetic First Name", "名フリガナ欄"),
    ("Name Suffix", "敬称"),
    ("Nickname", "ニックネーム"),
    ("Organization Name", "会社名(空欄多)"),
    ("Organization Title", "役職(空欄多)"),
    ("Notes", "メモ"),
    ("Labels", "ラベル/グループ"),
    ("E-mail 1 - Value", "メール1"),
    ("E-mail 2 - Value", "メール2"),
    ("Phone 1 - Label", "電話1種別"),
    ("Phone 1 - Value", "電話1"),
    ("Phone 2 - Label", "電話2種別"),
    ("Phone 2 - Value", "電話2"),
    ("Address 1 - Formatted", "住所"),
    ("Birthday", "誕生日"),
]

with open(SRC, encoding="utf-8-sig", newline="") as f:
    rows = list(csv.DictReader(f))

with open(DST, "w", encoding="utf-8-sig", newline="") as f:
    w = csv.writer(f)
    w.writerow(["No"] + [jp for _, jp in COLMAP])
    for i, r in enumerate(rows, 1):
        w.writerow([i] + [(r.get(src) or "").strip() for src, _ in COLMAP])

print(f"件数: {len(rows)}")
print(f"出力: {DST}")
