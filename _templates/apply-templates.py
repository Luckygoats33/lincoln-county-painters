"""
Apply header and footer templates to all HTML pages.
Replaces everything from <header to </div> (mobile overlay end)
and from <footer to </footer> with the template versions,
adjusting {PREFIX} per file depth.

Usage: py -3 _templates/apply-templates.py
"""
import os
import re
import glob

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEMPLATES = os.path.join(ROOT, '_templates')

def get_depth(filepath):
    rel = os.path.relpath(os.path.dirname(filepath), ROOT)
    if rel == '.':
        return 0
    return len(rel.replace('\\', '/').split('/'))

def make_prefix(depth):
    if depth == 0:
        return ''
    return '../' * depth

# Read templates
with open(os.path.join(TEMPLATES, 'header.html'), 'r', encoding='utf-8') as f:
    header_tpl = f.read().strip()

with open(os.path.join(TEMPLATES, 'footer.html'), 'r', encoding='utf-8') as f:
    footer_tpl = f.read().strip()

html_files = glob.glob(os.path.join(ROOT, '**', '*.html'), recursive=True)
# Exclude templates themselves
html_files = [f for f in html_files if '_templates' not in f]

header_fixed = 0
footer_fixed = 0
header_failed = []
footer_failed = []

for filepath in sorted(html_files):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    original = content
    rel = os.path.relpath(filepath, ROOT)
    depth = get_depth(filepath)
    prefix = make_prefix(depth)

    # Build this page's header and footer
    page_header = header_tpl.replace('{PREFIX}', prefix)
    page_footer = footer_tpl.replace('{PREFIX}', prefix)

    # --- HOMEPAGE SPECIAL CASE ---
    # Homepage has non-solid nav (no nav-solid class) for transparent hero
    if rel == 'index.html':
        page_header = page_header.replace('class="nav nav-solid"', 'class="nav"')
        # Homepage estimate link points to #estimate instead of contact/
        page_header = page_header.replace(
            f'href="{prefix}contact/" class="btn btn-accent btn-sm">Free Estimate',
            'href="#estimate" class="btn btn-accent btn-sm">Free Estimate'
        )
        # Mobile overlay estimate also points to #estimate
        page_header = page_header.replace(
            f'href="{prefix}contact/" class="btn btn-accent btn-lg"',
            'href="#estimate" class="btn btn-accent btn-lg"'
        )

    # --- REPLACE HEADER ---
    # Match from <header class="nav to end of mobile-overlay </div>
    header_pattern = r'<header class="nav[^>]*>.*?</div>\s*\n\s*</header>\s*\n\s*<div class="mobile-overlay"[^>]*>.*?</div>'
    header_match = re.search(header_pattern, content, re.DOTALL)
    if header_match:
        content = content[:header_match.start()] + page_header + content[header_match.end():]
        header_fixed += 1
    else:
        header_failed.append(rel)

    # --- REPLACE FOOTER ---
    footer_pattern = r'<footer class="footer">.*?</footer>'
    footer_match = re.search(footer_pattern, content, re.DOTALL)
    if footer_match:
        content = content[:footer_match.start()] + page_footer + content[footer_match.end():]
        footer_fixed += 1
    else:
        footer_failed.append(rel)

    if content != original:
        with open(filepath, 'w', encoding='utf-8', newline='\n') as f:
            f.write(content)

print(f"Headers: {header_fixed} updated, {len(header_failed)} failed")
if header_failed:
    for f in header_failed[:5]:
        print(f"  HEADER FAIL: {f}")

print(f"Footers: {footer_fixed} updated, {len(footer_failed)} failed")
if footer_failed:
    for f in footer_failed[:5]:
        print(f"  FOOTER FAIL: {f}")

print(f"\nTotal: {len(html_files)} files processed")
