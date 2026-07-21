# 連絡先_Outlook用.csv を「Yomi Company Name」→「Yomi Last Name」の順に並べ替える。
# 読み（フリガナ）はカタカナなので、そのままの文字列ソートで五十音順になる。
# 空欄の Yomi Company Name / Yomi Last Name はそれぞれ末尾にまとめる。
import csv, sys

PATH = "project/連絡先/連絡先_Outlook用.csv"

with open(PATH, encoding="utf-8-sig", newline="") as f:
    reader = csv.reader(f)
    header = next(reader)
    rows = list(reader)

ci = header.index("Yomi Company Name")
li = header.index("Yomi Last Name")

def key(row):
    comp = row[ci].strip()
    last = row[li].strip()
    # 空欄は末尾へ（フラグ 1 が後ろ）
    return (1 if not comp else 0, comp, 1 if not last else 0, last)

rows.sort(key=key)

with open(PATH, "w", encoding="utf-8-sig", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(header)
    writer.writerows(rows)

print(f"並べ替え完了: {len(rows)}件")
