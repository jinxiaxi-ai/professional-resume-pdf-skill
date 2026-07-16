# Professional Resume PDF Skill

A reusable Codex Skill for turning Chinese or bilingual resume content into a polished one-to-two-page A4 PDF. It preserves the user's wording by default, supports clickable contact links, and includes deterministic render and verification scripts.

The bundled template uses fictional content and a generic portrait placeholder. It contains no real resume, portrait, employer history, phone number, email address, or personal domain.

## What it does

- creates a professional navy-and-white resume layout;
- keeps company, role, and date visually distinct;
- preserves bold labels inside experience bullets;
- produces clickable phone, email, and portfolio links;
- supports single-field updates and role-specific variants;
- renders A4 PDFs through Chrome or Chromium;
- renders page PNGs with Poppler for visual QA;
- verifies page count, required text, forbidden text, and URI annotations.

## Install

```bash
git clone https://github.com/jinxiaxi-ai/professional-resume-pdf-skill.git
mkdir -p ~/.codex/skills
cp -R professional-resume-pdf-skill/skills/build-professional-resume-pdf ~/.codex/skills/
```

Restart Codex after installation if the new skill is not detected immediately.

## Use

Invoke the skill explicitly:

```text
Use $build-professional-resume-pdf to format this Markdown resume as a polished two-page PDF. Preserve all wording and make the portfolio URL clearly clickable.
```

Other example requests:

```text
Use $build-professional-resume-pdf to update only the dates in my existing resume and keep the prior PDF for rollback.
```

```text
Use $build-professional-resume-pdf to create a second version where one job title changes, without modifying any other content.
```

## Manual render

Requirements:

- Python 3.10+
- Google Chrome or Chromium
- Poppler (`pdftoppm`) for PNG previews
- `pypdf` for automated PDF checks

```bash
cd skills/build-professional-resume-pdf
python3 scripts/render_resume.py \
  --input assets/resume-template.html \
  --output tmp/example-resume.pdf \
  --render-dir tmp/rendered

python3 scripts/verify_pdf.py tmp/example-resume.pdf \
  --expected-pages 2 \
  --required-text "示例姓名" \
  --required-uri "https://example.com/"
```

## Repository structure

```text
skills/build-professional-resume-pdf/
├── SKILL.md
├── agents/openai.yaml
├── assets/
│   ├── portrait-placeholder.svg
│   └── resume-template.html
├── references/
│   └── customization-and-qa.md
└── scripts/
    ├── render_resume.py
    └── verify_pdf.py
```

## Privacy

Do not commit a real resume, portrait, generated PDF, browser profile, or task-local working directory to a public fork. The included `.gitignore` blocks common generated and personal artifact formats, but always inspect staged changes before publishing.

## License

MIT
