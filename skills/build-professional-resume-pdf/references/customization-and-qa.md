# Customization and QA Reference

## Contents

1. Editing the template
2. Typography and spacing
3. Fitting dense content
4. Links and portraits
5. Visual QA
6. Public-repository privacy

## Editing the template

Copy the HTML and SVG assets into a task-local directory before editing. Replace the fictional example content section by section. Duplicate or remove complete `.education-item`, `.entry`, and `.project` blocks; do not leave unmatched tags.

Keep content and formatting changes separate. When a user requests one textual change, extract text from the previous and new PDF, normalize whitespace, and confirm that the new text equals the old text with only the requested replacement.

Use `<strong>` for short bullet prefixes such as `数据分析：` rather than bolding an entire paragraph. Keep company name, role, descriptor, and date in `.entry-head` so they stay visually connected.

## Typography and spacing

The public template uses this fallback stack:

```css
font-family: "Microsoft YaHei", "PingFang SC", "Noto Sans CJK SC", Arial, sans-serif;
```

Do not publish Microsoft YaHei or other proprietary font files. If the user owns a locally installed font, add a local `@font-face` rule only in the task copy.

Recommended starting values:

- Body: 12px, 21px line height
- Name: 28px
- Section title: 16px
- Company/school/project title: 13px
- Side padding: 10mm
- Work bullet gap: 1.8mm
- Entry header-to-body gap: 2mm

Change one spacing variable at a time and re-render. A one-pixel font change can alter many line wraps.

## Fitting dense content

Use this order when content does not fit:

1. Reduce excessive paragraph or entry margins by 0.2–0.4mm.
2. Reduce section-title top/bottom margins slightly.
3. Reduce line height by 1px while keeping body text at 12px.
4. Reduce side padding only if the page still looks balanced.
5. Reduce body size to 11.5px or 11px only as a last resort.

Never hide overflow, clip text, or create a near-empty extra page to claim the resume fits. If the user authorizes content editing, suggest concise rewrites separately from the styling pass.

## Links and portraits

- Phone: `href="tel:+8613800000000"`
- Email: `href="mailto:name@example.com"`
- Homepage: use the exact confirmed target, including `https://` or `http://`
- Visible homepage text may omit the scheme, but the `href` must not.
- Use only the homepage link color in the top bar when the user wants other contact text to remain black.

For portraits, use a supplied local file and an absolute file URI or copy the image next to the HTML. Preserve aspect ratio with `object-fit: cover`. Remove the portrait column and identity offset together when no portrait is wanted.

## Visual QA

Render every page to PNG at 150–180 DPI and inspect it at full size. Confirm:

- no clipped or overlapping text;
- no heading stranded at the bottom of a page;
- every company header has visible space before its first bullet;
- dates align consistently on the right;
- bold bullet labels remain visibly distinct;
- work bullets are black and other navigational bullets use the accent color;
- the portfolio link is visibly clickable;
- the last page does not contain an avoidable large blank area;
- text remains readable at normal PDF zoom.

Use `verify_pdf.py` after visual inspection. Text extraction cannot prove layout quality.

## Public-repository privacy

Before staging files, scan the entire repository and Git history for:

- real names and usernames;
- phone numbers and email addresses;
- personal domains and social links;
- employer and school combinations tied to a person;
- portrait or screenshot files;
- absolute local paths containing a real username;
- generated PDFs, DOCX files, browser profiles, and temporary render directories;
- API keys, tokens, cookies, and authentication logs.

Use fictional examples such as `示例姓名`, `示例大学`, `示例科技有限公司`, `name@example.com`, and `https://example.com/`. Run a final `rg` scan and inspect `git diff --cached` before publishing.
