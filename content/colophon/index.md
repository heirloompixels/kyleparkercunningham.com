+++
title = "Colophon"
template = "page.html"

[extra]
label = "How This Site Is Made"
+++

This site is a long‑term archive built to outlast trends. It is a static site with minimal dependencies, designed for clarity, speed, and future portability.

## Principles
- Minimal, typography‑first presentation
- No JavaScript
- Content as durable text and images
- Fluid type and spacing scales (Utopia)
- Works remain the primary subject

## Stack
- **Generator:** Zola
- **Typography:** Literata (body + headings), IBM Plex Sans (UI + captions), Inconsolata (code)
- **Layout:** CSS custom properties with fluid scales
- **Images:** Original assets preserved; resized variants generated at build time

## Style Guide

### Headings
# H1 — The archive begins here
## H2 — The work in context
### H3 — A quiet subheading

### Paragraph
The archive favors quiet, declarative prose. It privileges clarity and the subtle rhythm of long‑form text over ornament. The goal is to read without friction.

### Links
A link should be visible without being loud. [This is a link example](/oeuvre/).

### Lists
- This is a list item
- Another list item
- A third list item

1. This is a numbered list
2. Another item
3. A final item

### Blockquote
> The archive exists to hold the work in a steady light.

### Code
Inline code looks like `resize_image` and code blocks are quiet and legible:

```text
./scripts/build.sh
```

### Table
| Field | Purpose | Example |
| --- | --- | --- |
| `year` | When the work was made | 2024 |
| `medium` | Materials used | Oil on canvas |
| `status` | Availability | sold |

### Figure
{{ art_image(path="oeuvre/painting/2024/the-river-in-the-sky/the-river-in-the-sky.jpg", alt="Oil painting with luminous cloud forms and a strip of blue sky.", caption="Example figure with caption.") }}

### Small text
<small>Small text can be used for quiet notes or metadata.</small>

## Updates
This colophon will evolve as the archive grows.
