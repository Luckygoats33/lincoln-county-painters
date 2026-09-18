#!/usr/bin/env python3
"""
Lincoln County Painters — Blog Post Generator
Generates 103 SEO-optimized blog post HTML files + blog index page.
"""
import os
import sys
import importlib.util

PROJECT_DIR = r"C:\Users\willw\Projects\lincoln-county-painters"
BLOG_DIR = os.path.join(PROJECT_DIR, "blog")
SCRATCHPAD = r"C:\Users\willw\AppData\Local\Temp\claude\C--Users-willw\6b8d022b-ba5d-4222-9743-cc0cf3fd34e0\scratchpad"

# --- Load batch files ---
def load_batch(filename):
    path = os.path.join(SCRATCHPAD, filename)
    spec = importlib.util.spec_from_file_location(filename.replace('.py', ''), path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.POSTS

ALL_POSTS = []
for batch_file in ['batch1.py', 'batch2.py', 'batch3.py', 'batch4.py']:
    try:
        ALL_POSTS.extend(load_batch(batch_file))
    except Exception as e:
        print(f"Error loading {batch_file}: {e}")
        sys.exit(1)

print(f"Loaded {len(ALL_POSTS)} posts total")

# --- HTML Templates ---

NAV = '''<header class="nav nav-solid" id="nav">
  <div class="nav-inner">
    <a href="/" class="nav-logo"><span class="nav-logo-mark">LCP</span><span class="nav-logo-text">Lincoln County<br>Painters</span></a>
    <nav class="nav-links"><a href="/services/">Services</a><a href="/service-areas/">Areas</a><a href="/projects/">Projects</a><a href="/cost/">Cost</a><a href="/about/">About</a><a href="/contact/">Contact</a></nav>
    <div class="nav-actions">
      <a href="tel:5412707341" class="nav-phone">(541) 270-7341</a>
      <a href="/contact/" class="btn btn-accent btn-sm">Free Estimate</a>
    </div>
    <button class="nav-toggle" id="navToggle" aria-label="Open menu"><span></span><span></span><span></span></button>
  </div>
</header>
<div class="mobile-overlay" id="mobileNav">
  <button class="mobile-close" id="mobileClose" aria-label="Close menu"><svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/></svg></button>
  <a href="/services/">Services</a><a href="/service-areas/">Areas</a><a href="/projects/">Projects</a><a href="/cost/">Cost</a><a href="/about/">About</a><a href="/contact/">Contact</a>
  <a href="tel:5412707341">(541) 270-7341</a>
  <a href="/contact/" class="btn btn-accent btn-lg" style="margin-top:16px">Get Free Estimate</a>
</div>'''

FOOTER = '''<footer class="footer">
  <div class="container">
    <div class="footer-grid">
      <div class="footer-brand">
        <div style="display:flex;align-items:center;gap:10px;margin-bottom:16px">
          <span style="font-family:'Newsreader',serif;font-weight:700;font-size:1.3rem;background:var(--wave);color:#fff;width:38px;height:38px;display:flex;align-items:center;justify-content:center;border-radius:6px">LCP</span>
          <span style="font-family:'Newsreader',serif;font-weight:600;font-size:.9rem;color:#fff;line-height:1.2">Lincoln County<br>Painters</span>
        </div>
        <p>Interior and exterior painting for homes and businesses on the Central Oregon Coast.</p>
      </div>
      <div><h4>Services</h4><ul class="footer-links"><li><a href="/services/interior-painting/">Interior</a></li><li><a href="/services/exterior-painting/">Exterior</a></li><li><a href="/services/residential-painting/">Residential</a></li><li><a href="/services/commercial-painting/">Commercial</a></li><li><a href="/services/cabinet-painting/">Cabinets</a></li><li><a href="/services/deck-fence-staining/">Deck &amp; Fence</a></li></ul></div>
      <div><h4>Service Areas</h4><ul class="footer-links"><li><a href="/service-areas/newport-or/">Newport</a></li><li><a href="/service-areas/lincoln-city-or/">Lincoln City</a></li><li><a href="/service-areas/depoe-bay-or/">Depoe Bay</a></li><li><a href="/service-areas/waldport-or/">Waldport</a></li><li><a href="/service-areas/yachats-or/">Yachats</a></li><li><a href="/service-areas/toledo-or/">Toledo</a></li><li><a href="/service-areas/siletz-or/">Siletz</a></li></ul></div>
      <div><h4>Contact</h4>
        <p><a href="tel:5412707341" style="color:rgba(255,255,255,.7)">(541) 270-7341</a></p>
        <p style="color:rgba(255,255,255,.7)">info@LincolnCountyPainters.com</p>
        <p style="color:rgba(255,255,255,.7)">Lincoln County, Oregon</p>
        <ul class="footer-links" style="margin-top:16px"><li><a href="/blog/">Blog</a></li><li><a href="/about/">About</a></li><li><a href="/contact/">Contact</a></li></ul>
      </div>
    </div>
    <div class="footer-bottom"><span>&copy; 2026 Lincoln County Painters</span><span>Interior &amp; Exterior Painting &middot; Central Oregon Coast</span></div>
  </div>
</footer>'''

def post_html(post):
    slug = post['slug']
    title = post['title']
    category = post['category']
    meta_desc = post['meta_description']
    content = post['content']

    # Escape title for OG
    og_title = title.replace('"', '&quot;')
    og_desc = meta_desc.replace('"', '&quot;')

    return f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title} | Lincoln County Painters Blog</title>
<meta name="description" content="{meta_desc}">
<link rel="canonical" href="https://www.lincolncountypainters.com/blog/{slug}/">
<meta property="og:type" content="article">
<meta property="og:title" content="{og_title}">
<meta property="og:description" content="{og_desc}">
<meta property="og:url" content="https://www.lincolncountypainters.com/blog/{slug}/">
<meta property="og:site_name" content="Lincoln County Painters">
<meta name="twitter:card" content="summary">
<meta name="robots" content="index,follow">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Newsreader:ital,opsz,wght@0,6..72,400;0,6..72,500;0,6..72,600;0,6..72,700;1,6..72,400&family=Outfit:wght@300;400;500;600;700&display=swap">
<link rel="stylesheet" href="../../styles.css">
</head>
<body>

{NAV}

<article class="blog-post">
  <div class="container">
    <div class="blog-post-header">
      <div class="eyebrow">{category}</div>
      <h1>{title}</h1>
      <p class="blog-meta">Lincoln County Painters</p>
    </div>
    <div class="blog-content">
      {content}
    </div>
    <div class="blog-cta">
      <h2>Ready to Get Started?</h2>
      <p>Contact Lincoln County Painters for a free estimate on your next painting project.</p>
      <a href="/contact/" class="btn btn-accent">Get a Free Estimate</a>
      <a href="tel:5412707341" class="btn btn-outline-dark">Call (541) 270-7341</a>
    </div>
  </div>
</article>

{FOOTER}

<script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@type": "Article",
  "headline": "{og_title}",
  "description": "{og_desc}",
  "author": {{
    "@type": "Organization",
    "name": "Lincoln County Painters",
    "url": "https://www.lincolncountypainters.com/"
  }},
  "publisher": {{
    "@type": "Organization",
    "name": "Lincoln County Painters"
  }},
  "mainEntityOfPage": {{
    "@type": "WebPage",
    "@id": "https://www.lincolncountypainters.com/blog/{slug}/"
  }}
}}
</script>
<script src="../../script.js"></script>
</body>
</html>'''


def blog_index_html(posts):
    # Group by category
    categories = {}
    for p in posts:
        cat = p['category']
        if cat not in categories:
            categories[cat] = []
        categories[cat].append(p)

    # Category order
    cat_order = [
        'Coastal Painting', 'Interior Painting', 'Exterior Painting',
        'Cabinet Painting', 'Deck & Fence', 'Commercial Painting',
        'Cost & Value', 'Seasonal & Timing', 'City Guide', 'How-To & Education'
    ]

    # Build filter buttons
    filter_buttons = '<button class="active" data-filter="all">All Posts</button>\n'
    for cat in cat_order:
        if cat in categories:
            filter_id = cat.lower().replace(' & ', '-').replace(' ', '-')
            filter_buttons += f'      <button data-filter="{filter_id}">{cat}</button>\n'

    # Build cards
    cards_html = ''
    for cat in cat_order:
        if cat not in categories:
            continue
        filter_id = cat.lower().replace(' & ', '-').replace(' ', '-')
        for p in categories[cat]:
            cards_html += f'''      <a href="/blog/{p["slug"]}/" class="blog-card" data-category="{filter_id}">
        <div class="blog-card-body">
          <div class="blog-card-category">{p["category"]}</div>
          <h3>{p["title"]}</h3>
          <p>{p["meta_description"][:120]}...</p>
        </div>
        <span class="blog-card-link">Read More &rarr;</span>
      </a>
'''

    return f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Painting Blog | Lincoln County Painters</title>
<meta name="description" content="Expert painting tips, guides, and advice for Oregon Coast homeowners. Learn about interior painting, exterior coatings, cabinet refinishing, deck staining, and more.">
<link rel="canonical" href="https://www.lincolncountypainters.com/blog/">
<meta property="og:type" content="website">
<meta property="og:title" content="Painting Blog | Lincoln County Painters">
<meta property="og:description" content="Expert painting tips, guides, and advice for Oregon Coast homeowners from Lincoln County Painters.">
<meta property="og:url" content="https://www.lincolncountypainters.com/blog/">
<meta property="og:site_name" content="Lincoln County Painters">
<meta name="twitter:card" content="summary">
<meta name="robots" content="index,follow">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Newsreader:ital,opsz,wght@0,6..72,400;0,6..72,500;0,6..72,600;0,6..72,700;1,6..72,400&family=Outfit:wght@300;400;500;600;700&display=swap">
<link rel="stylesheet" href="../styles.css">
</head>
<body>

{NAV}

<section class="blog-hero">
  <div class="container">
    <div class="eyebrow">Our Blog</div>
    <h1>Painting Tips &amp; Guides</h1>
    <p>Expert advice for homeowners on the Central Oregon Coast. From prep to finish, salt air to interior design.</p>
  </div>
</section>

<section class="section" style="padding-top:0">
  <div class="container">
    <div class="blog-categories">
      {filter_buttons}
    </div>
    <div class="blog-grid" id="blogGrid">
{cards_html}
    </div>
  </div>
</section>

<section class="cta-band">
  <div class="container">
    <h2>Ready to Transform Your Home?</h2>
    <p>Contact Lincoln County Painters for a free, no-obligation estimate on your next painting project.</p>
    <a href="/contact/" class="btn btn-accent btn-lg">Get a Free Estimate</a>
    <a href="tel:5412707341" class="btn btn-outline btn-lg">Call (541) 270-7341</a>
  </div>
</section>

{FOOTER}

<script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@type": "Blog",
  "name": "Lincoln County Painters Blog",
  "description": "Expert painting tips and guides for Oregon Coast homeowners.",
  "url": "https://www.lincolncountypainters.com/blog/",
  "publisher": {{
    "@type": "Organization",
    "name": "Lincoln County Painters",
    "url": "https://www.lincolncountypainters.com/"
  }}
}}
</script>
<script src="../script.js"></script>
<script>
(function(){{
  var buttons = document.querySelectorAll('.blog-categories button');
  var cards = document.querySelectorAll('.blog-card');
  buttons.forEach(function(btn){{
    btn.addEventListener('click', function(){{
      var filter = btn.dataset.filter;
      buttons.forEach(function(b){{ b.classList.remove('active'); }});
      btn.classList.add('active');
      cards.forEach(function(card){{
        if (filter === 'all' || card.dataset.category === filter) {{
          card.style.display = '';
        }} else {{
          card.style.display = 'none';
        }}
      }});
    }});
  }});
}})();
</script>
</body>
</html>'''


# --- Generate files ---
def main():
    # Create blog directory
    os.makedirs(BLOG_DIR, exist_ok=True)

    # Generate each post
    for i, post in enumerate(ALL_POSTS):
        slug = post['slug']
        post_dir = os.path.join(BLOG_DIR, slug)
        os.makedirs(post_dir, exist_ok=True)
        filepath = os.path.join(post_dir, 'index.html')
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(post_html(post))
        print(f"  [{i+1:3d}/{len(ALL_POSTS)}] blog/{slug}/index.html")

    # Generate blog index
    index_path = os.path.join(BLOG_DIR, 'index.html')
    with open(index_path, 'w', encoding='utf-8') as f:
        f.write(blog_index_html(ALL_POSTS))
    print(f"\n  Blog index: blog/index.html")

    print(f"\nDone! Generated {len(ALL_POSTS)} blog posts + 1 index page.")

if __name__ == '__main__':
    main()
