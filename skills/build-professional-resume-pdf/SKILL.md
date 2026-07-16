---
name: build-professional-resume-pdf
description: Create, restyle, or update polished Chinese or bilingual resume PDFs from Markdown, plain text, an existing resume, or structured career content. Use when Codex needs to build a professional one-to-two-page resume, preserve wording while improving visual hierarchy, update individual resume fields without disturbing layout, add clickable contact or portfolio links, generate role-specific variants, or render and visually verify an A4 PDF.
---

# Build Professional Resume PDF

Produce a concise A4 resume with strong hierarchy, compact spacing, clickable links, and deterministic visual QA. Preserve the user's wording unless they explicitly authorize content edits.

## Workflow

1. Read all source files and identify the authoritative content version.
2. Record the requested changes and distinguish content edits from style edits.
3. Copy `assets/resume-template.html` and `assets/portrait-placeholder.svg` into a task-local working directory.
4. Replace the fictional example content with the user's content. Keep section order unless the user asks to restructure it.
5. Preserve emphasized labels with `<strong>` and keep company, role, and date on one header row when space allows.
6. Replace the portrait source with the user's local image only when supplied. Otherwise retain the generic placeholder or remove the portrait cleanly.
7. Render the HTML with `scripts/render_resume.py`.
8. Inspect every rendered PNG page. Iterate until there is no clipping, overlap, orphan heading, accidental third page, or excessive blank area.
9. Run `scripts/verify_pdf.py` to confirm page count, required text, and clickable URIs.
10. Deliver a newly named PDF. Preserve the prior version when the user requests rollback support or a role-specific variant.

## Content Rules

- Do not invent, rewrite, shorten, or quantify achievements without explicit permission.
- Apply single-field changes literally and verify that no other extracted text changed.
- Treat the latest direct user correction as authoritative when it conflicts with an older source file.
- Keep dates in one consistent format, preferably `YYYY年MM月 - YYYY年MM月` for Chinese resumes.
- Add a space between Latin abbreviations and Chinese text where it improves readability, such as `AI 工具` and `SQL 模板`.
- Use explicit schemes in links: `mailto:`, `tel:`, and `https://` or a user-confirmed `http://` fallback.
- Publish only sanitized examples. Never add a real name, portrait, phone number, email address, home page, or employer history to a public repository without confirmation.

## Layout Rules

- Keep A4 pages at `210mm × 297mm` with `@page { margin: 0; }`.
- Start with 10mm side padding, 12px body text, and 21px line height.
- Use dark navy for section titles and company names, near-black body text, and pure-black work-experience bullets.
- Use blue and underline only for clearly clickable portfolio links in the top bar.
- Keep section bars, company headers, role names, dates, and bold bullet labels visually distinct.
- Prefer small spacing adjustments over shrinking body text below 11px.
- Keep work-experience headers attached to at least one following bullet.
- Avoid bundling proprietary fonts. Use the font stack in the template and configure a local `@font-face` only when the user's machine already has the font.

Read `references/customization-and-qa.md` before making structural layout changes, fitting unusually dense content, changing fonts, or preparing a public repository.

## Commands

Render a PDF and page previews:

```bash
python3 scripts/render_resume.py \
  --input assets/resume-template.html \
  --output tmp/resume.pdf \
  --render-dir tmp/rendered
```

Verify page count, content, and links:

```bash
python3 scripts/verify_pdf.py tmp/resume.pdf \
  --expected-pages 2 \
  --required-text "示例姓名" \
  --required-uri "https://example.com/"
```

If the environment provides bundled Python or Poppler binaries, prefer those paths over installing duplicate dependencies.

## Delivery Checklist

- Inspect every final page image at readable resolution.
- Confirm the PDF opens and has the intended page count.
- Confirm all requested text appears and superseded text does not.
- Confirm phone, email, and portfolio annotations contain the intended URIs.
- Confirm no real personal data remains in public assets, history, filenames, or generated artifacts.
- Provide a clickable absolute file link for local delivery, or the repository URL after publishing.
