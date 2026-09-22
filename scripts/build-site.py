#!/usr/bin/env python3
"""Build static Melania Inglessis portfolio pages from centralized data."""
from __future__ import annotations

import json
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1] / "template"
DATA = ROOT / "data"
OUT = ROOT

with open(DATA / "site.json", encoding="utf-8") as f:
    SITE = json.load(f)
with open(DATA / "projects.json", encoding="utf-8") as f:
    PROJECTS = sorted(json.load(f), key=lambda p: p.get("order", 999))
with open(DATA / "people.json", encoding="utf-8") as f:
    PEOPLE = sorted(json.load(f), key=lambda p: p.get("order", 999))
NEWS_PATH = DATA / "news.json"
NEWS = json.loads(NEWS_PATH.read_text(encoding="utf-8")) if NEWS_PATH.exists() else []

PROJECTS_BY_SLUG = {p["slug"]: p for p in PROJECTS}
PEOPLE_BY_SLUG = {p["slug"]: p for p in PEOPLE}


def rel(from_dir: Path, to: str) -> str:
    """Compute relative URL from an output directory to a site-root path."""
    depth = len(from_dir.relative_to(OUT).parts)
    prefix = "../" * depth if depth else ""
    return prefix + to


def asset(from_dir: Path, path: str | None) -> str:
    if not path:
        return ""
    return rel(from_dir, path)


def fonts_head() -> str:
    return """
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&family=Spline+Sans+Mono:wght@400;500&display=swap" rel="stylesheet">
<style>
  @font-face {
    font-family: "Inter Display";
    src: local("Inter Display"), local("Inter");
    font-weight: 400 600;
    font-display: swap;
  }
</style>
""".strip()


def media_block(src: str, alt: str, label: str) -> str:
    exists = (OUT / src).exists() if src and not src.startswith("http") else False
    # src is relative-from-page; existence check needs site-root path
    return f'<img src="{src}" alt="{alt}" loading="lazy">' if src else f'<div class="placeholder-img">{label}</div>'


def media_for(from_dir: Path, path: str | None, alt: str, label: str) -> str:
    if not path:
        return f'<div class="placeholder-img">{label}</div>'
    root_path = OUT / path
    href = asset(from_dir, path)
    if root_path.exists():
        return f'<img src="{href}" alt="{alt}" loading="lazy">'
    return f'<div class="placeholder-img" data-pending-src="{path}">{label}<br>asset pending</div>'


def nav(from_dir: Path, current: str) -> str:
    css = rel(from_dir, "css/site.css")
    brand_href = rel(from_dir, "index.html")
    work_href = rel(from_dir, "work.html")
    links = []
    mapping = [
        ("Home", "index.html", "home"),
        ("Work", "work.html", "work"),
        ("People", "people/index.html", "people"),
        ("News", "news.html", "news"),
        ("About", "about.html", "about"),
        ("Contact", "contact.html", "contact"),
    ]
    for label, href, key in mapping:
        url = rel(from_dir, href)
        cur = ' aria-current="page"' if current == key else ""
        links.append(f'<a href="{url}"{cur}>[{label.lower()}]</a>')
    social = f"""
      <div class="site-menu__social">
        <a href="{SITE['links']['instagram']}" target="_blank" rel="noopener">[instagram]</a>
        <a href="{SITE['links']['linkedin']}" target="_blank" rel="noopener">[linkedin]</a>
        <a href="{SITE['representation']['url']}" target="_blank" rel="noopener">[forward artists]</a>
      </div>
    """
    return f"""
<header class="site-nav">
  <a class="site-nav__brand" href="{brand_href}">{SITE['name']}</a>
  <div class="site-nav__meta" data-live-clock></div>
  <a class="site-nav__cta" href="{work_href}">[view work]</a>
  <button class="site-nav__toggle" type="button" aria-label="Open menu"><span></span><span></span><span></span></button>
</header>
<nav class="site-menu" aria-label="Primary">
  <div class="site-menu__inner">
    <h2 class="site-menu__title">Makeup Artist<span>Los Angeles / Worldwide</span></h2>
    <div>
      <div class="site-menu__links">
        {''.join(links)}
      </div>
      {social}
    </div>
  </div>
</nav>
"""


def footer(from_dir: Path) -> str:
    return f"""
<footer class="site-footer">
  <div>© {SITE['name']}</div>
  <div>{SITE['footerNote']}</div>
  <a href="{rel(from_dir, 'contact.html')}">Contact</a>
</footer>
<script src="{rel(from_dir, 'js/site.js')}" defer></script>
"""


def shell(title: str, description: str, from_dir: Path, current: str, body: str, og_image: str | None = None) -> str:
    css = rel(from_dir, "css/site.css")
    og = asset(from_dir, og_image) if og_image else ""
    og_tag = f'<meta property="og:image" content="{og}">' if og else ""
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{description}">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{description}">
{og_tag}
<meta name="theme-color" content="#000000">
{fonts_head()}
<link rel="stylesheet" href="{css}">
</head>
<body>
{nav(from_dir, current)}
{body}
{footer(from_dir)}
</body>
</html>
"""


def project_card(p: dict, from_dir: Path) -> str:
    href = rel(from_dir, f"work/{p['slug']}.html")
    cats = " ".join(p.get("categories") or [])
    year = p.get("year") or ""
    meta = " · ".join(x for x in [p.get("talent"), year, (p.get("categories") or [None])[0]] if x)
    media = media_for(from_dir, p.get("heroImage"), p.get("alt") or p["title"], p["title"])
    return f"""
<a class="card reveal" href="{href}" data-categories="{cats}">
  <div class="card__media">{media}</div>
  <h3 class="card__title">{p['title']}</h3>
  <p class="card__meta">{meta}</p>
</a>
"""


def person_card(person: dict, from_dir: Path) -> str:
    href = rel(from_dir, f"people/{person['slug']}.html")
    media = media_for(from_dir, person.get("heroImage"), person["name"], person["name"])
    badge = ' <span class="badge-archive">Archive</span>' if person.get("relationshipStatus") == "archive" else ""
    return f"""
<a class="card reveal" href="{href}">
  <div class="card__media">{media}</div>
  <h3 class="card__title">{person['name']}{badge}</h3>
  <p class="card__meta">{person['profession']}</p>
</a>
"""


def build_home():
    out = OUT / "index.html"
    tiles = []
    for slug in SITE["homepageProjectSlugs"]:
        p = PROJECTS_BY_SLUG[slug]
        href = f"work/{p['slug']}.html"
        media = media_for(OUT, p.get("heroImage"), p.get("alt") or p["title"], p["title"])
        fields = []
        if p.get("talent"):
            fields.append(f"<div><span>Talent</span>{p['talent']}</div>")
        if p.get("publication") or p.get("brand"):
            fields.append(f"<div><span>Publication</span>{p.get('publication') or p.get('brand')}</div>")
        if p.get("categories"):
            fields.append(f"<div><span>Category</span>{p['categories'][0]}</div>")
        if p.get("year"):
            fields.append(f"<div><span>Year</span>{p['year']}</div>")
        tiles.append(f"""
<a class="project-tile" href="{href}">
  <div class="project-tile__media">{media}</div>
  <div class="project-tile__content">
    <h2 class="project-tile__title">{p['title']}</h2>
    <div class="project-tile__meta">{''.join(fields)}</div>
  </div>
</a>
""")
    carousel_slugs = SITE.get("heroCarouselSlugs") or SITE["homepageProjectSlugs"][:5]
    slides = []
    dots = []
    first = PROJECTS_BY_SLUG[carousel_slugs[0]]
    first_meta = " · ".join(
        x for x in [first.get("talent"), first.get("publication") or first.get("brand"), first.get("year")] if x
    )
    for i, slug in enumerate(carousel_slugs):
        p = PROJECTS_BY_SLUG[slug]
        img = f"images/carousel/{slug}.jpg"
        if not (OUT / img).exists():
            img = p.get("heroImage")
        media = media_for(OUT, img, p.get("alt") or p["title"], p["title"])
        active = " is-active" if i == 0 else ""
        meta = " · ".join(
            x for x in [p.get("talent"), p.get("publication") or p.get("brand"), p.get("year")] if x
        )
        href = f"work/{p['slug']}.html"
        slides.append(
            f'<div class="hero-carousel__slide{active}" data-slide="{i}" '
            f'data-title="{p["title"]}" data-meta="{meta}" data-href="{href}">'
            f'<div class="hero-carousel__media">{media}</div></div>'
        )
        dots.append(
            f'<button type="button" class="hero-carousel__dot{active}" data-go="{i}" aria-label="Slide {i+1}"></button>'
        )
    body = f"""
<section class="hero-identity hero-identity--carousel">
  <div class="hero-carousel" data-hero-carousel>
    <div class="hero-carousel__track">{''.join(slides)}</div>
  </div>
  <div class="hero-identity__copy">
    <p class="hero-identity__role">{SITE['role']}</p>
    <h1 class="hero-identity__name">{SITE['name']}</h1>
    <p class="hero-identity__place">{SITE['location']}</p>
    <div class="hero-identity__project" data-hero-project>
      <a class="hero-identity__project-link" href="work/{first['slug']}.html" data-hero-link>
        <span class="hero-identity__project-title" data-hero-title>{first['title']}</span>
        <span class="hero-identity__project-meta" data-hero-meta>{first_meta}</span>
      </a>
    </div>
    <div class="hero-carousel__controls">
      <button type="button" class="hero-carousel__nav" data-hero-prev aria-label="Previous">←</button>
      <div class="hero-carousel__dots">{''.join(dots)}</div>
      <button type="button" class="hero-carousel__nav" data-hero-next aria-label="Next">→</button>
    </div>
  </div>
</section>
<section class="project-stack" id="work">
  {''.join(tiles)}
</section>
"""
    og_image = f"images/carousel/{carousel_slugs[0]}.jpg"
    if not (OUT / og_image).exists():
        og_image = first.get("heroImage")
    out.write_text(
        shell(
            f"{SITE['name']} | {SITE['role']}",
            SITE["tagline"],
            OUT,
            "home",
            body,
            og_image,
        ),
        encoding="utf-8",
    )


def build_work():
    out = OUT / "work.html"
    filters = "".join(
        f'<button type="button" data-filter="{c}" class="{"is-active" if c == "ALL" else ""}">{c}</button>'
        for c in SITE["categories"]
    )
    cards = "".join(project_card(p, OUT) for p in PROJECTS)
    body = f"""
<header class="page-header">
  <h1>Work</h1>
  <p><span data-work-count>{len(PROJECTS)}</span> projects</p>
</header>
<div class="filters" data-work-filters>{filters}</div>
<section class="work-grid" data-work-grid>
  {cards}
</section>
"""
    out.write_text(
        shell(f"Work | {SITE['name']}", f"Selected work by {SITE['name']}, makeup artist.", OUT, "work", body),
        encoding="utf-8",
    )


def build_project_pages():
    work_dir = OUT / "work"
    work_dir.mkdir(exist_ok=True)
    for old in work_dir.glob("*.html"):
        old.unlink()
    for p in PROJECTS:
        out = work_dir / f"{p['slug']}.html"
        meta_bits = []
        if p.get("talent"):
            meta_bits.append(f"<div><span>Talent</span>{p['talent']}</div>")
        if p.get("year"):
            year = p["year"]
            if p.get("month"):
                year = f"{p['month']} {year}"
            meta_bits.append(f"<div><span>Year</span>{year}</div>")
        if p.get("categories"):
            meta_bits.append(f"<div><span>Category</span>{', '.join(p['categories'])}</div>")
        if p.get("publication") or p.get("brand"):
            meta_bits.append(
                f"<div><span>Publication</span>{p.get('publication') or p.get('brand')}</div>"
            )
        if p.get("location"):
            meta_bits.append(f"<div><span>Location</span>{p['location']}</div>")

        summary = ""
        if p.get("summary"):
            summary = f'<section class="detail-copy"><h2>Overview</h2><p>{p["summary"]}</p></section>'
        beauty = ""
        if p.get("beautyNotes"):
            beauty = f'<section class="detail-copy"><h2>Beauty direction</h2><p>{p["beautyNotes"]}</p></section>'

        credits = ""
        if p.get("credits"):
            rows = "".join(
                f"<div><dt>{k}</dt><dd>{v}</dd></div>" for k, v in p["credits"].items() if v
            )
            credits = f'<section class="credits"><h2>Credits</h2><dl>{rows}</dl></section>'

        links = []
        if p.get("sourceUrl"):
            links.append(
                f'<a class="source-link" href="{p["sourceUrl"]}" target="_blank" rel="noopener">Primary source</a>'
            )
        for link in p.get("relatedLinks") or []:
            if link.get("url") and link.get("label"):
                links.append(
                    f'<a class="source-link" href="{link["url"]}" target="_blank" rel="noopener">{link["label"]}</a>'
                )
        people_links = []
        for slug in p.get("peopleSlugs") or []:
            person = PEOPLE_BY_SLUG.get(slug)
            if person:
                people_links.append(
                    f'<a class="source-link" href="{rel(work_dir, f"people/{slug}.html")}">{person["name"]}</a>'
                )
        links_html = ""
        if links or people_links:
            links_html = (
                '<section class="detail-links"><h2>Related</h2>'
                f'<div class="detail-links__row">{"".join(people_links + links)}</div></section>'
            )

        body = f"""
<section class="detail-hero">
  <div class="detail-hero__media">{media_for(work_dir, p.get('heroImage'), p.get('alt') or p['title'], p['title'])}</div>
  <div class="detail-hero__content">
    <h1>{p['title']}</h1>
    <div class="detail-meta">{''.join(meta_bits)}</div>
  </div>
</section>
<div class="detail-body">
  {summary}
  {beauty}
  {credits}
  {links_html}
</div>
"""
        out.write_text(
            shell(
                f"{p['title']} | {SITE['name']}",
                p.get("summary") or p.get("alt") or f"{p['title']} — makeup by {SITE['name']}",
                work_dir,
                "work",
                body,
                p.get("heroImage"),
            ),
            encoding="utf-8",
        )


def build_news():
    out = OUT / "news.html"
    items = []
    for n in NEWS:
        project = PROJECTS_BY_SLUG.get(n.get("projectSlug") or "")
        img_path = project.get("heroImage") if project else None
        media = media_for(OUT, img_path, n["title"], n["title"])
        project_link = (
            f'<a class="source-link" href="work/{project["slug"]}.html">View project</a>'
            if project
            else ""
        )
        source = (
            f'<a class="source-link" href="{n["sourceUrl"]}" target="_blank" rel="noopener">Source</a>'
            if n.get("sourceUrl")
            else ""
        )
        items.append(
            f"""
<article class="news-card reveal">
  <div class="news-card__media">{media}</div>
  <div class="news-card__body">
    <p class="news-card__meta">{n.get('date','')} · {n.get('category','')}</p>
    <h2 class="news-card__title">{n['title']}</h2>
    <p class="news-card__summary">{n.get('summary','')}</p>
    <div class="detail-links__row">{project_link}{source}</div>
  </div>
</article>
"""
        )
    body = f"""
<header class="page-header">
  <h1>News</h1>
  <p>Recent work & press · {len(NEWS)} updates</p>
</header>
<section class="news-feed">
  {''.join(items)}
</section>
"""
    og_image = None
    if NEWS:
        first_project = PROJECTS_BY_SLUG.get(NEWS[0].get("projectSlug") or "")
        if first_project:
            og_image = first_project.get("heroImage")
    out.write_text(
        shell(
            f"News | {SITE['name']}",
            f"Recent work and press for {SITE['name']}",
            OUT,
            "news",
            body,
            og_image,
        ),
        encoding="utf-8",
    )


def build_people_index():
    people_dir = OUT / "people"
    people_dir.mkdir(exist_ok=True)
    out = people_dir / "index.html"
    cards = "".join(person_card(person, people_dir) for person in PEOPLE)
    body = f"""
<header class="page-header">
  <h1>People</h1>
  <p>Artists Mélanie works with</p>
</header>
<section class="people-grid">
  {cards}
</section>
"""
    out.write_text(
        shell(f"People | {SITE['name']}", f"People directory — {SITE['name']}", people_dir, "people", body),
        encoding="utf-8",
    )


def build_people_pages():
    people_dir = OUT / "people"
    people_dir.mkdir(exist_ok=True)
    for person in PEOPLE:
        out = people_dir / f"{person['slug']}.html"
        # projects from person.projectSlugs OR projects that list this person
        slugs = list(person.get("projectSlugs") or [])
        for p in PROJECTS:
            if person["slug"] in (p.get("peopleSlugs") or []) and p["slug"] not in slugs:
                slugs.append(p["slug"])
        projects = [PROJECTS_BY_SLUG[s] for s in slugs if s in PROJECTS_BY_SLUG]
        cards = "".join(project_card(p, people_dir) for p in projects)
        archive = (
            ' <span class="badge-archive">Archive</span>'
            if person.get("relationshipStatus") == "archive"
            else ""
        )
        selected = (
            f'<section class="section-block"><h2>Selected work</h2><div class="work-grid">{cards}</div></section>'
            if projects
            else '<section class="section-block"><h2>Selected work</h2><p class="empty-note">Project imagery pending — relationship verified via Forward Artists roster.</p></section>'
        )
        body = f"""
<section class="person-hero">
  <div class="person-hero__media">{media_for(people_dir, person.get('heroImage'), person['name'], person['name'])}</div>
  <div class="person-hero__content">
    <h1>{person['name']}{archive}</h1>
    <p class="person-hero__role">{person['profession']}</p>
    <p class="person-hero__note">{person.get('summary','')}</p>
  </div>
</section>
{selected}
"""
        out.write_text(
            shell(
                f"{person['name']} | {SITE['name']}",
                f"Makeup work with {person['name']} by {SITE['name']}",
                people_dir,
                "people",
                body,
                person.get("heroImage"),
            ),
            encoding="utf-8",
        )


def build_about():
    out = OUT / "about.html"
    points = ["Celebrity", "Fashion", "Editorial", "Advertising", "Film", "Red carpet"]
    body = f"""
<div class="about-layout">
  <h1>About</h1>
  <p class="about-copy">{SITE['about']}</p>
  <div class="about-points">{''.join(f'<span>{p}</span>' for p in points)}</div>
  <p class="about-copy" style="font-size:1rem;color:var(--muted)">Biography synthesized from the Forward Artists profile for this independent portfolio concept. Not an official endorsement.</p>
  <a class="source-link" href="{SITE['links']['agencyPress']}" target="_blank" rel="noopener">Forward Artists profile</a>
</div>
"""
    out.write_text(
        shell(f"About | {SITE['name']}", SITE["about"][:160], OUT, "about", body),
        encoding="utf-8",
    )


def build_contact():
    out = OUT / "contact.html"
    body = f"""
<div class="contact-layout">
  <h1>Contact</h1>
  <p class="contact-rep">
    <span>{SITE['representation']['label']}</span>
    {SITE['representation']['name']}
  </p>
  <div class="contact-links">
    <a href="{SITE['representation']['url']}" target="_blank" rel="noopener">Forward Artists</a>
    <a href="{SITE['links']['agencyPress']}" target="_blank" rel="noopener">Press / profile</a>
    <a href="{SITE['links']['instagram']}" target="_blank" rel="noopener">Instagram</a>
    <a href="{SITE['links']['linkedin']}" target="_blank" rel="noopener">LinkedIn</a>
  </div>
</div>
"""
    out.write_text(
        shell(
            f"Contact | {SITE['name']}",
            f"Represented worldwide by Forward Artists — {SITE['name']}",
            OUT,
            "contact",
            body,
        ),
        encoding="utf-8",
    )


def main():
    # Remove obsolete Framer pages from publish root (kept under _framer-original)
    for name in [
        "work-grid.html",
        "work-list.html",
        "privacy-policy.html",
        "terms-of-use.html",
    ]:
        p = OUT / name
        if p.exists():
            p.unlink()
    works = OUT / "works-main"
    if works.exists():
        shutil.rmtree(works)

    build_home()
    build_work()
    build_project_pages()
    build_people_index()
    build_people_pages()
    build_news()
    build_about()
    build_contact()
    print(f"Built {len(PROJECTS)} projects, {len(PEOPLE)} people, {len(NEWS)} news")


if __name__ == "__main__":
    main()
