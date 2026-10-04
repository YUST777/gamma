#!/usr/bin/env python3
"""Read ICPC HUE Facebook posts from the user's already-open Chrome (CDP 9333).
Opens its own tab, scrolls the timeline, saves report/fb/posts.json + photos.
Never closes the browser."""
import json, os, re, sys, time, urllib.request
from datetime import datetime, timezone
sys.path.insert(0, os.path.dirname(__file__))
from fb_scrape import posts, parse_blob  # reuse parser

from playwright.sync_api import sync_playwright

OUT = 'report/fb'
SINCE = datetime(2025, 11, 1, tzinfo=timezone.utc).timestamp()
MAX_SCROLLS = int(sys.argv[1]) if len(sys.argv) > 1 else 400


def main():
    os.makedirs(OUT, exist_ok=True)
    gql = [0]
    with sync_playwright() as pw:
        browser = pw.chromium.connect_over_cdp('http://127.0.0.1:9333')
        ctx = browser.contexts[0]
        page = ctx.new_page()
        page.set_viewport_size({'width': 1280, 'height': 1000})

        def on_resp(r):
            if '/api/graphql' in r.url:
                gql[0] += 1
                try:
                    parse_blob(r.text())
                except Exception:
                    pass
        page.on('response', on_resp)
        page.goto('https://www.facebook.com/icpchue', wait_until='domcontentloaded')
        page.wait_for_timeout(6000)
        for blob in re.findall(r'<script type="application/json"[^>]*>(.*?)</script>', page.content(), re.S):
            parse_blob(blob)
        page.bring_to_front()
        stale, last = 0, 0
        for i in range(MAX_SCROLLS):
            page.keyboard.press('End')
            page.evaluate('window.scrollBy(0, document.body.scrollHeight)')
            page.wait_for_timeout(2200)
            dated = [p['time'] for p in posts.values() if p['time']]
            if i % 5 == 0:
                oldest = datetime.fromtimestamp(min(dated)).date() if dated else '-'
                print(f'scroll {i}: {len(posts)} posts, oldest {oldest}, gql {gql[0]}', flush=True)
            if dated and min(dated) < SINCE:
                print('reached Nov 2025'); break
            stale = stale + 1 if len(posts) == last else 0
            last = len(posts)
            if stale >= 25:
                print('no new posts loading, stopping'); break

        result = []
        for p in sorted(posts.values(), key=lambda p: p['time'] or 0):
            if not p['time']:
                continue
            day = datetime.fromtimestamp(p['time']).strftime('%Y-%m-%d')
            folder = f"{OUT}/{day}_{p['post_id']}"
            files = []
            for n, u in enumerate(p['images'], 1):
                os.makedirs(folder, exist_ok=True)
                f = f'{folder}/{n}.jpg'
                if not os.path.exists(f):
                    try:
                        urllib.request.urlretrieve(u, f)
                    except Exception:
                        continue
                files.append(f)
            result.append({'date': day, 'time': datetime.fromtimestamp(p['time']).strftime('%Y-%m-%d %H:%M'),
                           'post_id': p['post_id'], 'text': p['text'], 'photos': files})
        json.dump(result, open(f'{OUT}/posts.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
        print(f'Done: {len(result)} posts, {sum(len(r["photos"]) for r in result)} photos', flush=True)
        page.close()  # only our tab


if __name__ == '__main__':
    main()
