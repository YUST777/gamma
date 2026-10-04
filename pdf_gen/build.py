#!/usr/bin/env python3
"""Assemble HTML pages into one document and print it to PDF via headless Chrome.

Usage:
  python3 build.py en     # English edition (src_en/)
  python3 build.py old    # original 2025-2027 English report (src/)
  python3 build.py ar     # Arabic (standard) edition (src_ar/)
"""
import os
import glob
import subprocess
import sys

REPORTS = {
    'old': {
        'src': 'src',
        'pages': 17,
        'name': 'ICPC-HUE-Community-Progress-Report-Gamma-Style',
    },
    'ar': {
        'src': 'src_ar',
        'pages': 19,
        'name': 'ICPC-HUE-Report-AR-2025-2026',
    },
    'en': {
        'src': 'src_en',
        'pages': 19,
        'name': 'ICPC-HUE-Report-EN-2025-2026',
    },
    'eg': {
        'src': 'src_eg',
        'pages': 19,
        'name': 'ICPC-HUE-Report-EG-2025-2026',
    },
}


def build(key='en'):
    cfg = REPORTS[key]
    src = cfg['src']
    print(f"Assembling {cfg['pages']} pages from {src}/ into master HTML...")
    with open(f'{src}/header.html', 'r') as f:
        header = f.read()
    with open(f'{src}/footer.html', 'r') as f:
        footer = f.read()

    page_files = sorted(glob.glob(f'{src}/pages/page-*.html'))
    if len(page_files) != cfg['pages']:
        print(f"Warning: Expected {cfg['pages']} page files, found {len(page_files)}!")

    pages_content = []
    for pf in page_files:
        with open(pf, 'r') as f:
            pages_content.append(f.read().strip())

    master_html = header + "\n\n".join(pages_content) + "\n" + footer

    os.makedirs('output/html', exist_ok=True)
    os.makedirs('output/pdf', exist_ok=True)

    html_out = f"output/html/{cfg['name']}.html"
    pdf_out = f"output/pdf/{cfg['name']}.pdf"

    with open(html_out, 'w') as f:
        f.write(master_html)

    print(f"Wrote assembled HTML to {html_out} ({len(master_html)} bytes)")

    print("Compiling PDF via Headless Chrome...")
    cmd = [
        'google-chrome',
        '--headless',
        '--disable-gpu',
        '--no-pdf-header-footer',
        f'--print-to-pdf={pdf_out}',
        html_out
    ]
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode != 0:
        print("Error compiling PDF:", res.stderr)
        sys.exit(1)

    print(f"Successfully compiled PDF: {pdf_out}")

    info_res = subprocess.run(['pdfinfo', pdf_out], capture_output=True, text=True)
    for line in info_res.stdout.splitlines():
        if "Pages:" in line or "Page size:" in line:
            print(" ", line)


if __name__ == '__main__':
    build(sys.argv[1] if len(sys.argv) > 1 else 'en')
