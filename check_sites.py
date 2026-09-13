#!/usr/bin/env python3
"""
Script to fetch and check official olympiad websites for 2026/2027 schedule updates.
"""

import urllib.request
import ssl
import re
from datetime import datetime

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}

def parse_html_urls(filename='olympiads_2026_27.html'):
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()

    items = []
    tables = re.split(r'<h2', content)[1:]
    for t_idx, t_chunk in enumerate(tables):
        rows = re.findall(r'<tr([^>]*)>([\s\S]*?)</tr>', t_chunk)
        for r_attr, r_body in rows:
            if 'level-header' in r_attr or 'colspan' in r_body or '<th' in r_body:
                continue
            tds = re.findall(r'<td[^>]*>([\s\S]*?)</td>', r_body)
            if len(tds) >= 8:
                num = tds[0].strip()
                name_match = re.search(r'<a\s+href=\"([^\"]+)\"[^>]*>([\s\S]*?)</a>', tds[1])
                name = name_match.group(2).strip() if name_match else tds[1].strip()
                name = re.sub(r'<[^>]+>', '', name)
                url = name_match.group(1).strip() if name_match else ''
                is_2026 = 'season-2026' in r_attr
                items.append({
                    'table': t_idx + 1,
                    'num': num,
                    'name': name,
                    'url': url,
                    'is_2026': is_2026
                })
    return items

def check_url(url):
    if not url or not url.startswith('http'):
        return False, 0, "Invalid URL"
    try:
        req = urllib.request.Request(url, headers=HEADERS)
        with urllib.request.urlopen(req, context=ctx, timeout=8) as resp:
            data = resp.read().decode('utf-8', errors='ignore')
            text = re.sub(r'<script[\s\S]*?</script>', '', data)
            text = re.sub(r'<style[\s\S]*?</style>', '', text)
            text = re.sub(r'<[^>]+>', ' ', text)
            text = re.sub(r'\s+', ' ', text)

            matches = re.findall(r'(?:2026/2027|2026/27|2026-2027|2026–2027)', text)
            return True, len(matches), text
    except Exception as e:
        return False, 0, str(e)

def main():
    items = parse_html_urls()
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Checking {len(items)} olympiads...\n")

    for item in items:
        status, count, text_or_err = check_url(item['url'])
        if status:
            print(f"T{item['table']} #{item['num']} | 2026={item['is_2026']} | {item['name'][:35]} | Matches: {count}")
        else:
            print(f"T{item['table']} #{item['num']} | 2026={item['is_2026']} | {item['name'][:35]} | ERROR: {text_or_err}")

if __name__ == '__main__':
    main()
