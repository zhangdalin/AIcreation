#!/usr/bin/env python3
"""Convert all md files in composition/ to HTML files."""

import os
import glob
import markdown

COMPOSITION_DIR = os.path.join(os.path.dirname(__file__), "composition")
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "html_output")

HTML_TEMPLATE = """\
<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title}</title>
<style>
  body {{
    font-family: "Microsoft YaHei", "SimHei", "PingFang SC", "Noto Sans CJK SC", sans-serif;
    font-size: 16px;
    line-height: 1.9;
    color: #222;
    max-width: 800px;
    margin: 40px auto;
    padding: 0 24px 60px;
    background: #fff;
  }}
  h1 {{
    font-size: 1.8em;
    text-align: center;
    border-bottom: 2px solid #333;
    padding-bottom: 0.3em;
    margin-top: 1.5em;
  }}
  h2 {{
    font-size: 1.4em;
    border-left: 4px solid #555;
    padding-left: 10px;
    margin-top: 1.6em;
  }}
  h3 {{ font-size: 1.15em; margin-top: 1.3em; }}
  p {{
    text-indent: 2em;
    margin: 0.5em 0;
  }}
  blockquote {{
    border-left: 4px solid #aaa;
    margin: 1em 0;
    padding: 0.3em 1em;
    background: #f7f7f7;
    color: #555;
  }}
  table {{
    border-collapse: collapse;
    width: 100%;
    margin: 1em 0;
    font-size: 0.95em;
  }}
  th, td {{
    border: 1px solid #ccc;
    padding: 6px 12px;
    text-align: left;
  }}
  th {{
    background: #f0f0f0;
    font-weight: bold;
  }}
  tr:nth-child(even) {{ background: #fafafa; }}
  code {{
    background: #f0f0f0;
    padding: 1px 4px;
    border-radius: 3px;
    font-size: 0.9em;
  }}
  pre {{
    background: #f4f4f4;
    padding: 12px;
    overflow-x: auto;
    border-radius: 4px;
  }}
  hr {{
    border: none;
    border-top: 1px solid #ddd;
    margin: 2em 0;
  }}
  ul, ol {{
    padding-left: 2em;
  }}
  li {{ margin: 0.3em 0; }}
  strong {{ font-weight: bold; }}
  em {{ font-style: italic; }}
</style>
</head>
<body>
{body}
</body>
</html>
"""

EXTENSIONS = [
    "extra",        # tables, fenced_code, footnotes, attr_list, def_list, abbr
    "nl2br",        # newlines → <br>
    "sane_lists",   # better list handling
    "toc",          # auto heading anchors
]


def convert(md_path: str, out_path: str):
    with open(md_path, encoding="utf-8") as f:
        content = f.read()

    body_html = markdown.markdown(content, extensions=EXTENSIONS)
    title = os.path.splitext(os.path.basename(md_path))[0]

    full_html = HTML_TEMPLATE.format(title=title, body=body_html)

    with open(out_path, "w", encoding="utf-8") as f:
        f.write(full_html)


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    md_files = sorted(glob.glob(os.path.join(COMPOSITION_DIR, "*.md")))
    print(f"Found {len(md_files)} markdown files. Output → {OUTPUT_DIR}")

    for i, md_path in enumerate(md_files, 1):
        stem = os.path.splitext(os.path.basename(md_path))[0]
        out_path = os.path.join(OUTPUT_DIR, stem + ".html")
        convert(md_path, out_path)
        print(f"  [{i:02d}/{len(md_files)}] {os.path.basename(md_path)}  →  {stem}.html")

    print(f"\nDone! {len(md_files)} HTML files saved to: {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
