# Site Specification (v2)

## 1) Purpose & Audience
- **Purpose:** Definitive, lifelong archive of all works (art, projects, writings, photographs, etc.).
- **Audience:** Collectors and people interested in the work.
- **Core value:** Comprehensive, precise, searchable records per work, built to last decades.

## 2) Site Architecture

### 2.1 Oeuvre (Primary)
- **Primary name:** Oeuvre
- **Legacy synonyms/redirects:** Retained from prior slugs (aliases in frontmatter).
- **Scope:** Every work created.
- **Disciplines (current):**
  - painting
  - printmaking
  - sculpture
  - installations
  - exhibitions
  - other

### 2.2 Projects
- Projects are groupings of works across the archive.
- Each project includes:
  - artist statement / overview
  - exhibition information (if any)
  - linked works table with thumbnails and metadata
 - **Status values:** `ongoing`, `researching`, `complete`

### 2.3 Cinema
- Gallery of all video work with embeds and descriptions.

### 2.4 About
- Hub for biography, statement, process/materials, press, links, contact, etc.

### 2.5 Colophon
- Site principles, stack, and style guide samples.

## 3) Content Model (Universal Frontmatter for Works)
All Oeuvre works use the same schema for consistency and long‑term querying.

### 3.1 Universal Fields (Works)
- `title` (string, required)
- `year` (integer or string, required)
- `medium` (string or list)
- `discipline` (string; one of the archive sections)
- `dimensions` (string)
- `materials` (list)
- `edition` (string, optional)
- `status` (string; e.g. `available`, `sold`, `collection`, `unknown`)
- `location` (string, optional)
- `project` (list of project slugs, optional)
- `series` (string, optional)
- `description` (string, optional)
- `images` (list of filenames or paths)
- `tags` (list)
- `external_links` (list of `{ label, url }`)
- `aliases` (list; for legacy URL redirects)

### 3.2 Project Fields
- `title`
- `date`
- `template = "projects/single.html"`
- `[extra]`
  - `year` (integer or range string)
  - `status` (`ongoing`, `researching`, `complete`)
  - `cover` (relative path to cover image in project bundle)
  - `works` (list of Oeuvre work paths, e.g. `oeuvre/painting/2024/the-river-in-the-sky`)

### 3.3 Cinema Fields (Video)
- `title`
- `date` or `year`
- `duration` (optional)
- `format` (optional)
- `location` (optional)
- `embed` (YouTube/Vimeo URL)
- `description`
- `stills` (list)

## 4) File and Folder Structure

### 4.1 Oeuvre Works
Each work is a page bundle with co‑located images.
```
content/oeuvre/<discipline>/<year>/<slug>/index.md
content/oeuvre/<discipline>/<year>/<slug>/<image>.jpg
```

### 4.2 Projects
```
content/projects/_index.md
content/projects/<project-slug>/index.md
content/projects/<project-slug>/<images>
```

### 4.3 Cinema
```
content/cinema/index.md
content/cinema/<film-slug>/index.md
```

### 4.4 About
```
content/about/index.md
content/about/<topic>/index.md
```

### 4.5 Colophon
```
content/colophon/index.md
```

## 5) Navigation
**Main nav (top):**
- projects
- oeuvre
- painting
- printmaking
- cinema
- about

**Footer:**
- colophon
- home
- painting
- printmaking
- cinema
- about

## 6) Visual Direction
- Minimal, typography‑first, no JS.
- Utopia‑style fluid type & spacing scale.
- Literata (body + headings), IBM Plex Sans (UI + captions), Inconsolata (code).

## 7) Images
- **Originals preserved** in content bundles.
- **Responsive variants** generated at build time via `art_image` shortcode.
- **Shortcode:** `templates/shortcodes/art_image.html`
- **Sizes:** 480 / 960 / 1600 + original kept in content.

## 8) Home Page
- Landing page with hero and long-form, column-based layout.
- Content edited in `content/_index.md`.
- **Projects column:**
  - Present = 3 most recent projects with status `ongoing`
  - Future = all projects with status `researching`
  - Past = all projects with status `complete`
- **Recently edited list:** generated from file modification times for all `content/**/*.md`.

## 9) Project Layout
- Single-column project statement.
- Optional cover image.
- Works table with thumbnails and metadata.

## 10) Colophon & Style Guide
- Colophon includes a style guide section showing live typography samples.
- Content lives in `content/colophon/index.md`.

## 11) Roadmap (Next Phases)
- Complete metadata enrichment for all works.
- Expand projects with more linked works.
- Add cinema item pages with consistent metadata.
- Add archive utilities (indexes by year/medium/status).

## 12) Build & Deployment Automation
- **Recently edited generator:** `scripts/update_recently_edited.py`
- **Build wrapper:** `./scripts/build.sh` (runs the generator, then `zola build`)
- **Dev wrapper:** `./scripts/serve.sh` (runs the generator, then `zola serve`)
- **GitHub Pages:** `.github/workflows/main.yml` runs the generator before deploy, uses `GITHUB_TOKEN`.

## 13) Templates (Examples)

### Work Template
```
+++
title = "Work Title"
year = 2024
discipline = "painting"
medium = ["oil on canvas"]
dimensions = "24 x 36 in"
materials = ["oil", "linen", "wood frame"]
status = "available"
images = ["work-title.jpg"]
tags = ["landscape", "abstraction"]
+++

{{ art_image(path="oeuvre/painting/2024/work-title/work-title.jpg", alt="...", caption="...") }}
```

### Project Template
```
+++
title = "Project Title"
date = 2024-08-02
template = "projects/single.html"

[extra]
year = 2024
cover = "cover.jpg"
works = ["oeuvre/painting/2024/work-title"]
+++

Project statement.
```
