# -*- coding: utf-8 -*-
"""編集用マスターCSV → Outlookインポート用CSV(標準英語ヘッダ・BOM付)に変換する。

Outlook(デスクトップ / Outlook.com / Microsoft365)の連絡先インポートが
認識する標準列名で出力する。フリガナは Yomi 系の列に入れる。
"""
import csv, re

SRC = r"C:\Users\bwd001.BWD\OneDrive - bwd group\ドキュメント\Claude oguro\oguro-private\project\連絡先\連絡先_編集用マスター.csv"
DST = r"C:\Users\bwd001.BWD\OneDrive - bwd group\ドキュメント\Claude oguro\oguro-private\project\連絡先\連絡先_Outlook用.csv"

# Outlookインポートで一般的に認識される列（英語ヘッダ）
HEADERS = [
    "First Name","Middle Name","Last Name",
    "Yomi First Name","Yomi Last Name","Yomi Company Name",
    "Title","Suffix","Nickname",
    "Company","Department","Job Title",
    "File As",
    "E-mail Address","E-mail 2 Address","E-mail 3 Address",
    "Mobile Phone","Business Phone","Home Phone","Other Phone",
    "Business Street","Birthday","Categories","Notes",
]

# ラベルのうち残す価値のないもの（Googleの自動付与・整理用ゴミ）
LABEL_DROP = {"* myContacts", "* starred"}
def clean_categories(labels):
    cats = []
    for lab in (labels or "").split(" ::: "):
        lab = lab.strip()
        if not lab or lab in LABEL_DROP:
            continue
        if lab.startswith("インポート"):   # 「インポート: 1/25」等
            continue
        cats.append(lab)
    return ";".join(cats)

def map_phone(label):
    """電話種別ラベル → Outlookの電話列名。"""
    l = (label or "").lower()
    if "mobile" in l or "cell" in l or "携帯" in l:
        return "Mobile Phone"
    if "home" in l or "自宅" in l:
        return "Home Phone"
    if "work" in l or "business" in l or "勤務" in l:
        return "Business Phone"
    return "Other Phone"

with open(SRC, encoding="utf-8-sig", newline="") as f:
    rows = list(csv.DictReader(f))

out_rows = []
for r in rows:
    rec = {h: "" for h in HEADERS}
    rec["Last Name"]  = r.get("姓","").strip()
    rec["First Name"] = r.get("名","").strip()
    rec["Yomi Last Name"]  = r.get("姓フリガナ","").strip()
    rec["Yomi First Name"] = r.get("名フリガナ","").strip()
    rec["Company"]    = r.get("会社名","").strip()
    rec["Job Title"]  = r.get("役職","").strip()
    rec["Nickname"]   = r.get("ニックネーム","").strip()
    # 登録名(File As): 「会社名 姓名」→ Outlookで会社ごとにまとまり、中は姓順に並ぶ
    person = (rec["Last Name"] + rec["First Name"]).strip()
    rec["File As"] = " ".join(x for x in [rec["Company"], person] if x).strip()
    rec["E-mail Address"]   = r.get("メール1","").strip()
    rec["E-mail 2 Address"] = r.get("メール2","").strip()
    rec["E-mail 3 Address"] = r.get("メール3","").strip()
    rec["Business Street"]  = r.get("住所","").strip()
    rec["Birthday"]         = r.get("誕生日","").strip()
    rec["Categories"]       = clean_categories(r.get("ラベル",""))
    rec["Notes"]            = r.get("メモ","").strip()

    # 電話（種別で振り分け。同じ列が埋まっていたら Other へ退避）
    for label_key, val_key in [("電話1種別","電話1"), ("電話2種別","電話2")]:
        val = r.get(val_key,"").strip()
        if not val:
            continue
        col = map_phone(r.get(label_key,""))
        if rec[col]:
            col = "Other Phone" if not rec["Other Phone"] else "Business Phone"
        if rec[col]:
            # 全部埋まっていればメモに退避
            rec["Notes"] = (rec["Notes"] + f" / TEL:{val}").strip(" /")
        else:
            rec[col] = val

    out_rows.append([rec[h] for h in HEADERS])

with open(DST, "w", encoding="utf-8-sig", newline="") as f:
    w = csv.writer(f)
    w.writerow(HEADERS)
    w.writerows(out_rows)

print(f"変換件数: {len(out_rows)}")
print(f"出力: {DST}")
