# Resume Style System

Use this reference to preserve the bundled visual language while replacing all example content.

## Page and grid

- Page: A4 portrait, `210mm × 297mm`, with zero browser print margin.
- Page 1 padding: `9mm 10mm 10mm`; later pages start at `10mm` top padding.
- Default output: one or two pages. Keep explicit `.page` sections so page breaks are deterministic.
- Header: centered identity block plus an `18mm × 22mm` portrait slot.
- Company, role, and descriptor stay on the left; dates align to the right on the same baseline.

## Typography

- Preferred stack: Microsoft YaHei, PingFang SC, Noto Sans CJK SC, Arial, sans-serif.
- Do not distribute proprietary font files. Use a locally installed Microsoft YaHei only when available.
- Body: `12px` with `21px` line height.
- Name: `28px`, weight 700, `0.08em` letter spacing.
- Section title: `16px`, weight 700.
- School, company, and project title: `13px`, weight 700.
- Role and date: `12px`, weight 700 and 600 respectively.
- Bold only short semantic prefixes inside bullets. Keep paragraph bodies regular weight.

## Color tokens

The canonical values live in `assets/resume-style.css` under `:root`.

| Token | Value | Use |
| --- | --- | --- |
| Navy | `#0f4b83` | Section titles, schools, companies, projects |
| Link blue | `#075eb8` | Underlined homepage link only |
| Body ink | `#151b25` | Main text and numbered markers |
| Strong ink | `#070b12` | Bold bullet prefixes |
| Name ink | `#111827` | Name and role |
| Muted | `#5c6673` | Dates and project company |
| Section fill | `#ebf1f8` | Section title bar |
| Rules | `#d8e2ec` / `#d9e2ec` | Entry and header separators |

## Component rules

- Section bars use a pale-blue fill and a `1.2mm` navy left border.
- Work-experience markers are black. Summary, project, and skills markers use accent blue.
- Separate consecutive companies and projects with a thin gray rule.
- Keep a `2mm` gap between each work header and its first bullet.
- Make only the visible homepage URL blue and underlined when the remaining top bar is black.
- Use `.hero.no-portrait` and remove the image when a portrait is not wanted.
- Remove the homepage row completely when no homepage is supplied; do not leave an empty line.

## Adaptation boundaries

Preserve the palette, hierarchy, font scale, and row structure by default. Adapt only spacing variables when content density changes. Prefer reducing vertical margins in `0.2–0.4mm` steps, then line height by `1px`, before reducing body text below `12px`. Never go below `11px`, hide overflow, or shrink only one section enough to look inconsistent.
