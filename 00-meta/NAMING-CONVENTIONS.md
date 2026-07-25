---
id: meta-naming-conventions
title: Naming Conventions
type: standard
status: evergreen
version: 1.0
created: 2026-07-25
updated: 2026-07-25
tags: [meta, system, standards]
related: [meta-documentation-standard, meta-taxonomy]
---

# Naming Conventions v1.0

Names are the addresses of this repository. Stable names mean links never rot.

## Files

- `kebab-case.md` — lowercase, hyphens, no spaces, no underscores, no capitals.
- Descriptive and specific: `core-web-vitals.md`, not `cwv.md` or `performance.md`.
- No dates in filenames **except** in `60-journal/` and `70-radar/`, where the filename **is** the ISO date: `2026-07-25.md`.
- No version numbers in filenames. Versions live in frontmatter; the file path stays stable.
- `README.md` in every folder — capitalised, because GitHub renders it as the folder's index page.

## Folders

- Numbered prefixes at the top level (`00-`, `10-`, `15-`, `20-`…). Gaps are intentional: they let a new domain be inserted without renaming anything.
- Numbered prefixes inside `10-knowledge/` and `20-operations/` too, where reading order matters (`01-fundamentals/`, `02-technical-seo/`).
- Unnumbered elsewhere, where order does not matter (client names, industry names).
- `kebab-case` after the number prefix.

## IDs

Format: `prefix-slug`

- `prefix` comes from the controlled list in [TAXONOMY.md](./TAXONOMY.md) and tells you which folder the file lives in.
- `slug` matches the filename stem.
- Example: file `10-knowledge/02-technical-seo/crawl-budget.md` → id `tech-crawl-budget`.
- IDs are permanent. Titles can change; ids cannot.

## Client folders

`30-clients/client-name/` — the trading name in kebab-case. Never a project code you will forget. If a client must stay anonymous in public artifacts, the anonymised label is defined once in that client's README (`Client A — B2B SaaS, 40 employees`) and reused everywhere downstream.

## Dates

ISO 8601 everywhere: `2026-07-25`. Never `25/07/2026`, never `July 25`. Sortable by default, unambiguous across regions.

## Assets

Binaries live in `assets/` beside the note that references them, named after the note plus a descriptor: `crawl-budget-log-sample.png`.

## Reserved words

Do not name a file `index.md`, `notes.md`, `misc.md`, `temp.md`, `new.md`, or `untitled.md`. Every one of these becomes an unfindable dumping ground.
