# -*- coding: utf-8 -*-
"""漢字の姓・名からカタカナのフリガナを生成し、マスターに列を追加する。
- 姓フリガナ: 漢字からカタカナ生成（漢字が無ければ既存ローマ字をカナ変換）
- 名フリガナ: 新規にカタカナ生成（下の名前の読みは不確実 → 要確認フラグ）
- 既存のローマ字読みは「旧フリガナ(ローマ字)」列に保存（消さない）
"""
import csv, re
import pykakasi
import jaconv

MASTER = r"C:\Users\bwd001.BWD\OneDrive - bwd group\ドキュメント\Claude oguro\oguro-private\project\連絡先\連絡先_編集用マスター.csv"

_kks = pykakasi.kakasi()
_CJK = re.compile(r"[぀-ヿ㐀-䶿一-鿿]")

def to_kata_from_kanji(s):
    if not s:
        return ""
    return "".join(item["kana"] for item in _kks.convert(s))

def to_kata_from_romaji(s):
    if not s:
        return ""
    try:
        return jaconv.hira2kata(jaconv.alphabet2kana(s.lower()))
    except Exception:
        return ""

def has_kanji(s):
    return bool(_CJK.search(s or ""))

with open(MASTER, encoding="utf-8-sig", newline="") as f:
    reader = csv.DictReader(f)
    fields = list(reader.fieldnames)
    rows = list(reader)

# 列の再構成: 姓フリガナ(=カナに), 名フリガナ(新規), 旧フリガナ(ローマ字)(退避)
if "旧フリガナ(ローマ字)" not in fields:
    idx = fields.index("姓フリガナ")
    fields.insert(idx + 1, "名フリガナ")
    fields.append("旧フリガナ(ローマ字)")

gen_given = 0
for r in rows:
    old_romaji = r.get("姓フリガナ", "").strip()
    r["旧フリガナ(ローマ字)"] = old_romaji

    # 姓フリガナ（カタカナ）
    sei = r.get("姓", "").strip()
    if has_kanji(sei):
        r["姓フリガナ"] = to_kata_from_kanji(sei)
    elif old_romaji:
        r["姓フリガナ"] = to_kata_from_romaji(old_romaji)
    else:
        r["姓フリガナ"] = ""

    # 名フリガナ（カタカナ・新規生成）
    mei = r.get("名", "").strip()
    if has_kanji(mei):
        r["名フリガナ"] = to_kata_from_kanji(mei)
        gen_given += 1
        # 下の名前の読みは不確実 → フラグ追加
        cur = r.get("要確認", "").strip()
        tag = "名フリガナ自動生成(要確認)"
        r["要確認"] = (cur + " / " + tag).strip(" /") if cur else tag
    else:
        r["名フリガナ"] = ""

with open(MASTER, "w", encoding="utf-8-sig", newline="") as f:
    w = csv.DictWriter(f, fieldnames=fields)
    w.writeheader()
    w.writerows(rows)

print(f"名フリガナを生成した件数: {gen_given}")
print(f"列: {fields}")
