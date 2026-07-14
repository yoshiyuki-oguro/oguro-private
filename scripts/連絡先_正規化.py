# -*- coding: utf-8 -*-
"""Google連絡先CSVを「本来の欄」に正規化し、編集用マスターCSV(BOM付)を出力する。

現状ルール:
  First Name        = 担当者の名字（ローマ字＝名字の読み）
  Middle Name       = 担当者の氏名（漢字）※肩書き混入あり
  Last Name         = 企業名
  Phonetic Last/First = 企業名/名字ローマ字のコピー
  Name Suffix       = 敬称「様」

正規化方針:
  姓(Last Name)      ← 漢字氏名（肩書き除去後）。空白あれば前半、なければ全体
  名(First Name)     ← 漢字氏名の空白後半（なければ空）
  姓フリガナ          ← 名字ローマ字（＝名字の読み。元 First Name / Phonetic First Name）
  会社名(Org Name)   ← 企業名（元 Last Name）
  役職(Org Title)    ← 氏名から検出した肩書き
  敬称「様」          ← 削除
  電話/メール/住所/誕生日/ラベル/メモ/ニックネーム ← そのまま保持
  要確認             ← 姓名分割が未確定・データ異常のフラグ
"""
import csv, re
from namedivider import GBDTNameDivider

SRC = r"C:\Users\bwd001.BWD\OneDrive - bwd group\ドキュメント\Claude oguro\oguro-private\project\連絡先\contacts.csv"
DST = r"C:\Users\bwd001.BWD\OneDrive - bwd group\ドキュメント\Claude oguro\oguro-private\project\連絡先\連絡先_編集用マスター.csv"

# 姓名分割器（高精度GBDTモデル・完全ローカル処理）
_divider = GBDTNameDivider()
SCORE_THRESHOLD = 0.5  # これ未満は「分割自信低」として要確認に残す

def auto_split(kanji):
    """空白なし漢字氏名を姓名分割。(姓, 名, 確信度, 要確認理由) を返す。"""
    if len(kanji) < 3:
        return kanji, "", None, ""  # 2文字以下は名字のみとみなす
    try:
        r = _divider.divide_name(kanji)
    except Exception:
        return kanji, "", None, "自動分割エラー(要確認)"
    score = getattr(r, "score", None)
    reason = "" if (score is None or score >= SCORE_THRESHOLD) else f"分割自信低({score:.2f}・要確認)"
    return r.family, r.given, score, reason

TITLES = ["代表取締役","取締役","代表","会長","副社長","社長","専務","常務","本部長","事業部長",
          "部長代理","課長代理","次長","部長","課長","係長","主任","主査","主幹","室長","所長",
          "支店長","店長","工場長","統括","顧問","相談役","マネージャー","リーダー"]

def g(r,k): return (r.get(k) or "").strip()

_CJK = re.compile(r"[぀-ヿ㐀-䶿一-鿿]")
def has_cjk(s): return bool(_CJK.search(s or ""))

# 会社・屋号を示す接尾語（人名でなく会社名の連絡先を見分ける）
COMPANY_SUFFIX = ["工業所","自動車","建具店","建具","歯科","医院","クリニック","病院","外科","小児",
                  "税理士","会計","法律","石材","電機","産業","資材","商事","商会","工業","製作所",
                  "興業","運輸","運送","不動産","塗装","製材","木材"]
def looks_like_company(name):
    return any(s in name for s in COMPANY_SUFFIX)

def pick_name_fields(first, middle, ph_first):
    """First/Middle欄から「漢字氏名」と「ローマ字読み」を判定して返す。
    通常は Middle=漢字 / First=ローマ字 だが、逆に入力されたレコードもあるため中身で判定。"""
    fc, mc = has_cjk(first), has_cjk(middle)
    if mc and not fc:            # 通常パターン
        return middle, (first or ph_first)
    if fc and not mc:            # 逆パターン（漢字がFirst欄）
        return first, (middle or ph_first)
    if mc and fc:               # 両方に漢字 → Middleを氏名、Firstは読み扱い
        return middle, (ph_first or "")
    return "", (first or middle or ph_first)  # 漢字なし

def extract_title(kanji):
    """氏名文字列から肩書きを検出して (氏名, 役職) を返す。"""
    for t in TITLES:
        if t in kanji:
            name = kanji.replace(t, "").strip("　 ")
            return name, t
    return kanji, ""

def split_name(kanji):
    """漢字氏名を(姓, 名, 確信度, 要確認理由)に分割。"""
    if not kanji:
        return "", "", None, "漢字氏名が空"
    parts = re.split(r"[\s　]+", kanji)
    if len(parts) >= 2:
        # 元から空白あり → そのまま採用（分割済み・確信度は満点扱い）
        return parts[0], "".join(parts[1:]), None, ""
    # 会社名らしき文字列は人名分割しない
    if looks_like_company(kanji):
        return kanji, "", None, "会社名の可能性(氏名でない)"
    # 漢字を含まない（ローマ字のみ）→ 分割せず要確認
    if not has_cjk(kanji):
        return kanji, "", None, "漢字氏名でない(要確認)"
    # 空白なし漢字 → 自動分割
    return auto_split(kanji)

with open(SRC, encoding="utf-8-sig", newline="") as f:
    rows = list(csv.DictReader(f))

HEADERS = ["No","姓","名","姓フリガナ","会社名","役職","敬称(削除済)",
           "メール1","メール2","メール3","電話1種別","電話1","電話2種別","電話2",
           "住所","誕生日","ニックネーム","メモ","ラベル","分割確信度","要確認"]

out_rows = []
flag_count = 0
for i, r in enumerate(rows, 1):
    # First/Middle欄から漢字氏名とローマ字読みを判定（逆入力レコードも吸収）
    kanji_raw, romaji = pick_name_fields(
        g(r,"First Name"), g(r,"Middle Name"), g(r,"Phonetic First Name"))
    company = g(r,"Last Name")

    kanji, title = extract_title(kanji_raw)
    sei, mei, score, reason = split_name(kanji)

    flags = []
    if reason:
        flags.append(reason)
    # 敬称除去
    suffix = g(r,"Name Suffix")
    removed_suffix = suffix if suffix else ""
    # 漢字氏名が空でローマ字のみ → 姓にローマ字を暫定使用
    if not kanji_raw and romaji:
        sei = romaji
        romaji = ""  # 読み欄には残さない
        flags.append("漢字なし・ローマ字を姓に暫定")
    # フリガナ欄に電話番号など異常
    if re.search(r"\d{6,}", romaji):
        flags.append("フリガナ欄に数字混入")
    if flags:
        flag_count += 1

    out_rows.append([
        i, sei, mei, romaji, company, title, removed_suffix,
        g(r,"E-mail 1 - Value"), g(r,"E-mail 2 - Value"), g(r,"E-mail 3 - Value"),
        g(r,"Phone 1 - Label"), g(r,"Phone 1 - Value"),
        g(r,"Phone 2 - Label"), g(r,"Phone 2 - Value"),
        g(r,"Address 1 - Formatted"), g(r,"Birthday"),
        g(r,"Nickname"), g(r,"Notes"), g(r,"Labels"),
        (f"{score:.2f}" if score is not None else ""),
        " / ".join(flags),
    ])

with open(DST,"w",encoding="utf-8-sig",newline="") as f:
    w = csv.writer(f)
    w.writerow(HEADERS)
    w.writerows(out_rows)

print(f"総件数: {len(rows)}")
print(f"要確認フラグ付き: {flag_count}")
print(f"出力: {DST}")
