#!/usr/bin/env python3
"""Notion/Evernote書き出しHTMLから本文テキストだけを抽出する簡易ツール。
使い方: python html_to_text.py <input.html>
<article>...</article> 内のブロック要素をテキスト化して標準出力に出す。
"""
import sys
import re
import html


def main():
    if len(sys.argv) < 2:
        print("usage: python html_to_text.py <input.html>", file=sys.stderr)
        sys.exit(1)
    with open(sys.argv[1], encoding="utf-8") as f:
        src = f.read()

    # article本文だけを対象に（無ければ全体）
    m = re.search(r"<article\b[^>]*>(.*)</article>", src, re.S)
    body = m.group(1) if m else src

    # SVG / style / script を丸ごと除去
    body = re.sub(r"<svg\b.*?</svg>", " ", body, flags=re.S)
    body = re.sub(r"<style\b.*?</style>", " ", body, flags=re.S)
    body = re.sub(r"<script\b.*?</script>", " ", body, flags=re.S)

    # 画像は代替として [img:ファイル名] を残す
    def img_repl(mo):
        src_attr = re.search(r'src="([^"]*)"', mo.group(0))
        return f"\n[img: {src_attr.group(1)}]\n" if src_attr else "\n[img]\n"
    body = re.sub(r"<img\b[^>]*>", img_repl, body)

    # 見出し・リスト・段落の区切りで改行を入れる
    body = re.sub(r"</(p|li|h1|h2|h3|h4|div|figure|tr)>", "\n", body, flags=re.I)
    body = re.sub(r"<br\s*/?>", "\n", body, flags=re.I)
    body = re.sub(r"<li\b[^>]*>", "・", body, flags=re.I)
    body = re.sub(r"<h3\b[^>]*>", "\n### ", body, flags=re.I)
    body = re.sub(r"<h2\b[^>]*>", "\n## ", body, flags=re.I)
    body = re.sub(r"<h1\b[^>]*>", "\n# ", body, flags=re.I)

    # 残りのタグを除去
    text = re.sub(r"<[^>]+>", "", body)
    text = html.unescape(text)

    # 非改行スペース等を正規化
    text = text.replace("\xa0", " ")

    # 空行を圧縮
    lines = [ln.rstrip() for ln in text.splitlines()]
    out = []
    blank = 0
    for ln in lines:
        if ln.strip() == "":
            blank += 1
            if blank <= 1:
                out.append("")
        else:
            blank = 0
            out.append(ln)
    result = "\n".join(out).strip()

    # 出力先: 第2引数があればそこへ、無ければ標準出力(UTF-8)へ
    if len(sys.argv) >= 3:
        with open(sys.argv[2], "w", encoding="utf-8") as f:
            f.write(result)
    else:
        sys.stdout.reconfigure(encoding="utf-8")
        print(result)


if __name__ == "__main__":
    main()
