#!/usr/bin/env python3
"""Collect posts (date, text, photos) from the ICPC HUE Facebook page.

Opens a visible Chrome window. Log in to Facebook yourself; the script waits,
then scrolls the page timeline, reads the post data Facebook loads, and saves:
  report/fb/posts.json              one entry per post (date, text, photos)
  report/fb/<date>_<post_id>/N.jpg  the photos of each post
The login is kept in .fb_profile/ (delete it afterwards to log out).
"""
import json
import os
import re
import sys
import time
import urllib.request
from datetime import datetime, timezone

from playwright.sync_api import sync_playwright

PAGE_URL = 'https://www.facebook.com/icpchue'
OUT = 'report/fb'
PROFILE = '.fb_profile'
SCROLLS = int(sys.argv[1]) if len(sys.argv) > 1 else 120
SINCE = datetime(2025, 11, 1, tzinfo=timezone.utc).timestamp()

posts = {}


def walk(o):
    if isinstance(o, dict):
        yield o
        for v in o.values():
            yield from walk(v)
    elif isinstance(o, list):
        for v in o:
            yield from walk(v)


def harvest(obj):
    for d in walk(obj):
        if d.get('__typename') != 'Story' or not d.get('post_id'):
            continue
        pid = str(d['post_id'])
        ts, text, imgs = None, None, []
        for x in walk(d):
            if ts is None and isinstance(x.get('creation_time'), int):
                ts = x['creation_time']
            if text is None and isinstance(x.get('message'), dict) and isinstance(x['message'].get('text'), str):
                text = x['message']['text']
            for key in ('photo_image', 'image', 'viewer_image'):
                im = x.get(key)
                if isinstance(im, dict) and isinstance(im.get('uri'), str) and (im.get('height') or 0) >= 300:
                    if im['uri'] not in imgs:
                        imgs.append(im['uri'])
        p = posts.setdefault(pid, {'post_id': pid, 'time': None, 'text': '', 'images': []})
        p['time'] = p['time'] or ts
        p['text'] = p['text'] or (text or '')
        for u in imgs:
            if u not in p['images']:
                p['images'].append(u)


def parse_blob(body):
    for line in body.splitlines():
        line = line.strip()
        if not line.startswith('{'):
            continue
        try:
            harvest(json.loads(line))
        except Exception:
            pass


def main():
    os.makedirs(OUT, exist_ok=True)
    with sync_playwright() as pw:
        ctx = pw.chromium.launch_persistent_context(PROFILE, channel='chrome', headless=False,
                                                    viewport={'width': 1280, 'height': 900})
        page = ctx.pages[0] if ctx.pages else ctx.new_page()

        def on_resp(r):
            if '/api/graphql' in r.url:
                try:
                    parse_blob(r.text())
                except Exception:
                    pass
        page.on('response', on_resp)

        page.goto('https://www.facebook.com/login')
        print('Waiting for you to log in to Facebook in the opened window...', flush=True)
        for _ in range(900):
            if any(c['name'] == 'c_user' for c in ctx.cookies('https://www.facebook.com')):
                break
            time.sleep(1)
        else:
            print('Login not detected after 15 minutes, stopping.')
            return
        print('Logged in. Reading the page timeline...', flush=True)

        page.goto(PAGE_URL)
        page.wait_for_timeout(5000)
        for blob in re.findall(r'<script type="application/json"[^>]*>(.*?)</script>', page.content(), re.S):
            parse_blob(blob)

        stale = 0
        for i in range(SCROLLS):
            before = len(posts)
            page.mouse.wheel(0, 4000)
            page.wait_for_timeout(1800)
            dated = [p['time'] for p in posts.values() if p['time']]
            if i % 10 == 0:
                oldest = datetime.fromtimestamp(min(dated)).date() if dated else '-'
                print(f'scroll {i}: {len(posts)} posts, oldest {oldest}', flush=True)
            if dated and min(dated) < SINCE:
                break
            stale = stale + 1 if len(posts) == before else 0
            if stale >= 15:
                break

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
                try:
                    urllib.request.urlretrieve(u, f)
                    files.append(f)
                except Exception:
                    pass
            result.append({'date': day, 'post_id': p['post_id'], 'text': p['text'], 'photos': files})
        with open(f'{OUT}/posts.json', 'w', encoding='utf-8') as fh:
            json.dump(result, fh, ensure_ascii=False, indent=1)
        print(f'Done: {len(result)} posts, {sum(len(r["photos"]) for r in result)} photos -> {OUT}/posts.json')
        ctx.close()


if __name__ == '__main__':
    main()
