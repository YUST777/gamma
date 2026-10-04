#!/usr/bin/env python3
"""Screenshot icpchue.com pages through the already-open Chrome (CDP port 9333),
then frame each shot Gradia-style (yellow gradient, padding, rounded corners, shadow).
Never closes the user's browser: only the tabs this script opens.

Usage: python3 scripts/site_shots.py [route ...]
"""
import os
import sys

from PIL import Image, ImageDraw, ImageFilter
from playwright.sync_api import sync_playwright

BASE = 'https://www.icpchue.com'
RAW = 'report/assets/site/raw'
OUT = 'report/assets/site'
ROUTES = sys.argv[1:] or [
    '/', '/dashboard', '/dashboard/sessions', '/dashboard/sheets', '/dashboard/sheets/level-0',
    '/dashboard/leaderboard', '/dashboard/achievements', '/dashboard/roadmap', '/dashboard/profile',
    '/dashboard/discipline', '/dashboard/mentor', '/dashboard/news', '/dashboard/settings',
    '/devlog', '/fq', '/job', '/apply',
]


def slug(route):
    return (route.strip('/').replace('/', '_') or 'home')


def gradia_frame(src, dst, pad=110, radius=26):
    """Yellow diagonal gradient + rounded screenshot + soft shadow (matches public/*.png style)."""
    shot = Image.open(src).convert('RGB')
    w, h = shot.size
    W, H = w + pad * 2, h + pad * 2
    bg = Image.new('RGB', (W, H))
    top, bot = (250, 204, 21), (234, 179, 8)
    px = bg.load()
    for y in range(H):
        for x in range(0, W, 4):
            t = (x / W + y / H) / 2
            c = tuple(int(top[i] + (bot[i] - top[i]) * t) for i in range(3))
            for k in range(4):
                if x + k < W:
                    px[x + k, y] = c
    mask = Image.new('L', (w, h), 0)
    ImageDraw.Draw(mask).rounded_rectangle((0, 0, w, h), radius, fill=255)
    shadow = Image.new('L', (W, H), 0)
    ImageDraw.Draw(shadow).rounded_rectangle((pad, pad + 18, pad + w, pad + h + 18), radius, fill=120)
    shadow = shadow.filter(ImageFilter.GaussianBlur(28))
    bg.paste(Image.new('RGB', (W, H), (90, 60, 0)), (0, 0), shadow)
    bg.paste(shot, (pad, pad), mask)
    bg.save(dst, quality=90)


def main():
    os.makedirs(RAW, exist_ok=True)
    with sync_playwright() as pw:
        browser = pw.chromium.connect_over_cdp('http://127.0.0.1:9333')
        ctx = browser.contexts[0]
        for r in ROUTES:
            page = ctx.new_page()
            try:
                page.set_viewport_size({'width': 1440, 'height': 900})
                page.goto(BASE + r, wait_until='networkidle', timeout=45000)
                page.wait_for_timeout(2500)
                raw = f'{RAW}/{slug(r)}.png'
                page.screenshot(path=raw)
                gradia_frame(raw, f'{OUT}/{slug(r)}.jpg')
                print('ok ', r, '->', page.url, flush=True)
            except Exception as e:
                print('ERR', r, e, flush=True)
            finally:
                page.close()
        # do NOT call browser.close(): it would close the user's Chrome


if __name__ == '__main__':
    main()
