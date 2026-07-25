---
id: meta-documentation-standard
title: Documentation Standard
type: standard
status: evergreen
version: 1.0
created: 2026-07-25
updated: 2026-07-25
tags: [meta, system, standards]
related: [meta-naming-conventions, meta-taxonomy]
---

# Documentation Standard v1.0

Every Markdown file in this repository follows this standard. No exceptions, including quick notes. A quick note that skips frontmatter is a note that cannot be found in two years.

---

## 1. Frontmatter

Every file opens with a YAML block between `---` fences.

```yaml
---
id: tech-crawl-budget          # unique, permanent, kebab-case, prefix from TAXONOMY
title: Crawl Budget            # human title, Title Case
type: concept                  # see type list below
status: seed                   # seed | growing | evergreen | deprecated
version: 1.0                   # required for template/sop/checklist/deliverable; optional elsewhere
created: 2026-07-25            # ISO 8601, never changes
updated: 2026-07-25            # ISO 8601, bump on every edit
tags: [technical-seo, crawling]
prerequisites: [tech-crawling]                                  # what to understand first
related: [tech-robots-txt, tech-xml-sitemap]                     # sideways connections
next: [tech-log-file-analysis]                                   # what this unlocks
sources: []                                                      # URLs or citations
owner: me                                                        # me | client-name
---
```

### Field rules

- `id` is **permanent**. Rename the title freely; never change an id, because other files point at it.
- `updated` is bumped on every meaningful edit. A typo fix does not count.
- `prerequisites`, `related`, `next` hold **ids**, not file paths. The ids resolve via the taxonomy prefix to a folder.
- Unused fields are omitted, not left empty. Do not carry `sources: []` if you have no sources.

### Allowed `type` values

`concept` · `hub` · `standard` · `sop` · `checklist` · `template` · `deliverable` · `framework` · `playbook` · `case-study` · `portfolio` · `client-doc` · `simulation` · `content-asset` · `journal` · `review` · `radar` · `prompt` · `tool` · `reference` · `glossary`

---

## 2. Body structure by type

### `concept` — the encyclopedia entry

```markdown
# Title

> One-sentence definition. Written so a client could understand it.

## Why it matters
Business impact in plain language. Why anyone should care.

## How it works
The mechanics. Diagrams, tables, examples.

## How I apply it
My own practical method. This section is what separates my notes from a blog post.

## Common mistakes
What goes wrong, including mistakes I have made. Link to the mistake journal entry.

## Connections
- **Prerequisites:** [[links]]
- **Related:** [[links]]
- **Next:** [[links]]
- **Used in:** SOPs, playbooks, deliverables that depend on this

## Sources
## Changelog
- 2026-07-25 — v1.0 created
```

### `sop` — a repeatable process

`Purpose` → `When to run this` → `Inputs required` → `Steps` (numbered, each with expected output) → `Definition of done` → `Common failure points` → `Linked checklist` → `Linked deliverable template` → `Changelog`

### `checklist` — pure verification

Flat or grouped GitHub task lists (`- [ ]`). Every item is binary: either done or not. No prose. If an item needs explanation, it belongs in the SOP and the checklist links to it.

### `template` / `deliverable` — a blank to be filled

Fill-in markers in `{{DOUBLE_BRACES}}`. An `## Instructions` block at the top, wrapped in an HTML comment so it disappears from the client-facing render. Versioned, always: a deliverable sent to a client must be traceable to the template version that produced it.

### `journal` / `review` / `radar` — dated entries

Filename is the ISO date. Body follows the matching template. Append-only: never rewrite history, add a correction note instead.

---

## 3. Status lifecycle

| Status | Meaning | Standard |
|---|---|---|
| `seed` | Captured, incomplete, may be wrong | Fine to be rough. Must still have frontmatter |
| `growing` | Actively being developed and tested in real work | Definition and mechanics are correct |
| `evergreen` | I can teach this from memory and defend it to a client | Complete, linked, no known gaps |
| `deprecated` | No longer true or no longer used | Must state **why** and link to what replaced it. Moves to `90-archive/` |

Promotion is deliberate. Reviewed during the weekly review.

---

## 4. Versioning

- **Concepts** use `updated` plus a changelog line. No semantic version needed; understanding evolves continuously.
- **Templates, SOPs, checklists, deliverables** use `MAJOR.MINOR`:
  - MINOR: wording, formatting, added optional section.
  - MAJOR: the structure changed, or the output a client receives changed materially.
- Client deliverables record the template version used, in the deliverable itself.

---

## 5. Linking

Two link styles, both required:

1. **Relative Markdown links** in body prose: `[Crawl Budget](../10-knowledge/02-technical-seo/crawl-budget.md)`. These work on GitHub, which matters because GitHub is the fallback that never breaks.
2. **Frontmatter ids** in `prerequisites` / `related` / `next`. These are the machine-readable graph.

**Bidirectional rule:** if A lists B as `related`, add A to B's `related`. Links are declared on both ends, or the map has one-way streets. Checked during the weekly review.

---

## 6. Tags

Tags come from the controlled vocabulary in [TAXONOMY.md](./TAXONOMY.md). Inventing a tag is allowed, but it must be added to the taxonomy in the same commit. Aim for 2–5 tags per file; ten tags mean none of them mean anything.

---

## 7. Non-negotiables

- Markdown only for knowledge. Binaries (PDFs, screenshots, exports) live in an `assets/` subfolder beside the note that uses them.
- No client-confidential data outside `30-clients/`. Redaction happens before anything moves to `40-portfolio/`.
- No file is created from scratch. Copy from [templates/](./templates/).
- Nothing is deleted. It is deprecated and archived.
