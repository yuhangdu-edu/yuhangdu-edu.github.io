# Site Handoff — yuhangdu-edu.github.io

Personal academic website for **Yuhang Du**, PhD candidate in Management Science & Operations at London Business School. Drop this file into a new chat to skip re-scanning the repo.

## Stack
- **Jekyll** via `github-pages` gem (no version lock); theme is a detached **Academic Pages** fork (Minimal Mistakes lineage).
- Kramdown (GFM) + Rouge; Sass/SCSS with Susy grid; vanilla JS (no bundler).
- Local dev: `bundle install && bundle exec jekyll serve` — or Docker (`Dockerfile`, `docker-compose.yaml`) / Dev Container (`.devcontainer/`).
- Deploy: GitHub Pages from `master`. One custom Action: [.github/workflows/scrape_talks.yml](.github/workflows/scrape_talks.yml) (auto-scrapes talks).

## Site metadata ([_config.yml](_config.yml))
- `title: "Yuhang Du"` · `url: https://yuhangdu-edu.github.io` · `baseurl: ""`
- Author: PhD candidate, MS&O, LBS · London · `ydu@london.edu` · avatar `profile.jpg`
- Socials enabled: SSRN, LinkedIn (others commented out)
- Comments disabled; `jekyll-feed`, `jekyll-sitemap`, `jekyll-redirect-from`, `jemoji`

## Navigation ([_data/navigation.yml](_data/navigation.yml))
About (`/`) · Research (`/research/`) · In the Field (`/field/`) · Talks (`/talks/`) · Teaching (`/teaching/`)

## Pages ([_pages/](_pages/))
| File | What it is |
|---|---|
| [about.md](_pages/about.md) | Homepage bio — PhD candidate focus on maternal/perinatal health ops; field work in Liberia, Kenya, NHS |
| [research.md](_pages/research.md) | 3 papers: 1 published (PLoS One), 1 major revision at *OR*, 1 in prep. Links birth-analytics.org |
| [field.md](_pages/field.md) | **Rich interactive page** — tabbed (Liberia active / Cambridge "Coming soon"), photo gallery + lightbox, accordion for two tools: **SBA Wheel** and **Artemis** web app (https://artemis-inky.vercel.app/dashboard) |
| [talks.md](_pages/talks.md) | INFORMS, POMS, MSOM Healthcare appearances |
| [teaching.md](_pages/teaching.md) | TA roles at LBS (Data/Business/Decision Analytics) + Shanghai Uni |
| [cv.md](_pages/cv.md) / [cv-json.md](_pages/cv-json.md) | CV (markdown or JSON Resume via [_data/cv.json](_data/cv.json)) |
| [publications.html](_pages/publications.html) | Archive grouped by category (books / manuscripts / conferences) |

## Collections (declared [_config.yml](_config.yml) L223-235)
- `_publications/` · `_talks/` · `_teaching/` · `_portfolio/` — all `output: true`, permalink `/:collection/:path/`
- Layout defaults: `single`, author_profile on ([_config.yml](_config.yml) L239-293)

## Data ([_data/](_data/))
- `navigation.yml` — header nav
- `cv.json` — JSON Resume schema (feeds cv-json.md)
- `ui-text.yml` — i18n strings (en variants)
- `authors.yml` — template stubs, unused
- `comments/` — Staticman artifacts, unused

## Custom work beyond stock Academic Pages
- **[_includes/sba-wheel.html](_includes/sba-wheel.html)** + **[assets/js/sba-wheel.js](assets/js/sba-wheel.js)** — 2400×2400 canvas, 22-sector wheel, drag/touch rotation, nulliparous/multiparous layer toggle, PNG image layers in [images/](images/).
- **[assets/css/main.scss](assets/css/main.scss) L45-251** — field-page styles: `.field-tabs__*`, `.field-gallery-*` (horizontal scroll), `.field-accordion-*`, `.field-lightbox-*`; wide-content tweak >925px.
- [_layouts/single.html](_layouts/single.html) L50-60 — multi-link support (paperurl + slidesurl + bibtexurl together).

## Content-generation scripts ([markdown_generator/](markdown_generator/))
TSV → per-file markdown pipeline. Not auto-run; invoke manually when bulk-adding.
- `publications.py` / `publications.ipynb` ← `publications.tsv`
- `talks.py` / `talks.ipynb` ← `talks.tsv`
- `pubsFromBib.py` / `OrcidToBib.ipynb` — Bibtex / ORCID pipelines

## Recent iteration focus (last ~15 commits → Apr 13, 2026)
1. Content edits to [talks.md](_pages/talks.md), [research.md](_pages/research.md), [field.md](_pages/field.md).
2. SBA-wheel image debugging — pixel-level PPTX→PNG geometry fixes on `layer1_nuli.png` / `layer1_multi.png` ("hole 0" flood-fill corrections).
3. [main.scss](assets/css/main.scss) styling iterations for field page.

## Gotchas
- `files/` directory does **not** exist — some PDF links still point at upstream academicpages template URLs.
- Cambridge/NHS tab on field page is a placeholder.
- `_portfolio/` and `_posts/` are template examples, not real content.
- SBA wheel PNGs are high-DPI (2400px) and geometry-sensitive — edit with care.

## Owner context
5th-year PhD (as of Apr 2026). Advisors: Jérémie Gallien, Qi (George) Chen. BS from Shanghai Uni (2021). Collaborators include MoH Liberia, NHS, CHAI.
