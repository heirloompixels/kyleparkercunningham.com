# Site Specification (v1)

## 1) Purpose & Audience
- **Purpose:** Definitive, lifelong archive of all works (art, projects, writings, photographs, etc.).
- **Audience:** Collectors and people interested in your work.
- **Core value:** Comprehensive, precise, searchable records per work, built to last decades.

## 2) Site Architecture

### 2.1 Catalog Raisonne (Primary)
- **Primary name:** Catalog Raisonne
- **Legacy synonym:** Oeuvre (redirects preserved)
- **Scope:** Every work you have created.
- **Disciplines (initial):**
  - painting
  - printmaking
  - sculpture
  - installations
  - writing
  - photography
  - metalsmithing
  - drawing
  - bookbinding

### 2.2 Cinema
- A gallery of all video work.
- Each entry includes embeds, stills, and metadata.

### 2.3 Projects
- Projects are groupings of works across the catalog.
- Each project includes:
  - overview / statement
  - installation photos
  - links to related works

### 2.4 About
- Hub for biography, statement, process/materials, press, links, contact, etc.

## 3) Content Model (Universal Frontmatter)
All works use the same schema to support consistency and long-term querying.

### 3.1 Universal Fields (Works)
- `title` (string, required)
- `year` (integer or string, required)
- `medium` (string or list)
- `discipline` (string; one of the catalog sections)
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

### 3.2 Cinema Fields (Videos)
- `title`
- `year`
- `duration`
- `format`
- `location`
- `embed` (YouTube/Vimeo URL)
- `description`
- `stills` (list)

### 3.3 Project Fields
- `title`
- `year`
- `location`
- `works` (list of work slugs)
- `installation_images` (list)
- `statement`

## 4) File and Folder Structure

### 4.1 Works
- Each work is a page bundle:
  - `content/catalog-raisonne/<discipline>/<year>/<slug>/index.md`
  - Images are co-located in the same folder.

Example:
```
content/catalog-raisonne/painting/2024/the-river-in-the-sky/index.md
content/catalog-raisonne/painting/2024/the-river-in-the-sky/the-river-in-the-sky.jpg
```

### 4.2 Cinema
```
content/cinema/index.md
content/cinema/<project-or-film-slug>/index.md
```

### 4.3 Projects
```
content/projects/_index.md
content/projects/<project-slug>/index.md
```

### 4.4 About
```
content/about/index.md
content/about/<topic>/index.md
```

## 5) Naming Conventions
- Slugs are lowercase, hyphenated, stable over time.
- Filenames for images match the work title when possible.
- Avoid renaming after publication unless unavoidable.

## 6) Content Workflow

### 6.1 Backlog Ingestion
- Batch upload works by discipline and year.
- Normalize metadata to the universal frontmatter schema.
- Co-locate images with each work.

### 6.2 Ongoing Additions
- Use a simple template per work.
- Fill at least: `title`, `year`, `discipline`, `images`.
- Add more metadata later if not available immediately.

### 6.3 Data Integrity
- Maintain consistent vocabularies for `status`, `discipline`, `materials`.
- Prefer `year` when exact date is unknown.
- Keep `project` references in sync with project pages.

## 7) Navigation
- Minimal top navigation:
  - home
  - painting
  - printmaking
  - cinema
  - about

## 8) Visual Direction
- Minimal, elegant, typography-first.
- No JavaScript.
- Works should be the focus, typography supports them.

## 9) Long-Term Maintainability
- All content stored as Markdown with consistent frontmatter.
- No dependencies on external APIs or JS.
- Portable as a static archive.

## 10) Roadmap (Phased)

### Phase 1: Catalog Foundation
- Standardize frontmatter schema in all work entries.
- Ensure all works are properly bundled with images.
- Verify redirects from `/oeuvre/` to `/catalog-raisonne/`.

### Phase 2: Project System
- Add `projects` section.
- Link project pages to individual works.

### Phase 3: Cinema Expansion
- Create individual cinema entries with consistent metadata.
- Add stills and contextual descriptions.

### Phase 4: Archive Utilities
- Index pages by year, medium, status.
- Add export-friendly views (print catalog, CSV exports, etc.).

## 11) Templates (Examples)

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

Short description or statement.
```

### Project Template
```
+++
title = "Project Title"
year = 2021
location = "Taos, NM"
works = ["work-slug-1", "work-slug-2"]
installation_images = ["install-1.jpg", "install-2.jpg"]
+++

Project overview.
```

### Cinema Template
```
+++
title = "Film Title"
year = 2022
duration = "7:32"
format = "HD video"
embed = "https://www.youtube.com/embed/XXXXX"
+++

Brief description.
```
