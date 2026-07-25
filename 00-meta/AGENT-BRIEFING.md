---
id: meta-agent-briefing
title: Agent Briefing — Paste This Into Any AI
type: standard
status: evergreen
version: 1.0
created: 2026-07-25
updated: 2026-07-25
tags: [meta, system]
related: [meta-documentation-standard, meta-taxonomy, meta-workflows]
---

# Agent Briefing

**Purpose:** this repository must never depend on one AI account, one chat history, or one vendor. This file is the portable context. Paste it into any assistant, on any account, and it will understand the system in one message.

Keep it updated whenever the structure changes. It is the single point of failure worth maintaining.

---

## Copy from here down

> I maintain a Markdown knowledge repository called **SEO Brain** — the permanent operating system for my SEO career. Before helping me, understand its rules. Follow them exactly; do not invent new structure.
>
> **Top-level folders**
> - `00-meta/` — system rules: documentation standard, templates, taxonomy, workflows, master knowledge map
> - `10-knowledge/` — evergreen SEO concepts, one file per concept, no dates, no client names
> - `15-business-playbooks/` — industry-specific reusable playbooks (law firms, dentists, SaaS, e-commerce, real estate, healthcare, education, restaurants, travel, local businesses)
> - `20-operations/` — SOPs, checklists, client deliverable templates, and an agency simulator for practice projects
> - `30-clients/` — one workspace per client, instantiated from the deliverable templates
> - `40-portfolio/` — sanitised case studies and portfolio samples
> - `50-content-engine/` — every concept turned into 11 teaching/marketing assets
> - `60-journal/` — dated daily learning log, mistake journal, weekly and monthly reviews
> - `70-radar/` — dated industry intelligence: Google updates, AI search changes, news
> - `80-library/` — prompts, tool profiles, frameworks, references, glossary
> - `90-archive/` — retired material. Nothing is ever deleted
>
> **Every file starts with YAML frontmatter:**
> ```yaml
> ---
> id: tech-crawl-budget      # permanent, kebab-case, domain prefix
> title: Crawl Budget
> type: concept              # concept|hub|sop|checklist|template|deliverable|framework|playbook|case-study|simulation|content-asset|journal|review|radar|prompt|tool|reference|glossary
> status: seed               # seed|growing|evergreen|deprecated
> version: 1.0
> created: 2026-07-25
> updated: 2026-07-25
> tags: [technical-seo, crawling]
> prerequisites: [tech-crawling]
> related: [tech-robots-txt]
> next: [tech-log-file-analysis]
> ---
> ```
>
> **Concept body sections, in this order:** Definition (one sentence) → Why it matters → How it works → How I apply it → Common mistakes → Connections → Sources → Changelog.
>
> **Rules you must respect:**
> 1. One canonical location per asset. Never duplicate; link instead.
> 2. Links are declared on both ends. If A relates to B, B relates to A.
> 3. `id` values are permanent. Titles may change, ids never.
> 4. Filenames are `kebab-case.md`, no dates — except journal and radar files, which are named `YYYY-MM-DD.md`.
> 5. Every folder has a `README.md` acting as its hub and index.
> 6. Nothing is deleted. Outdated material is marked `deprecated` and moved to `90-archive/`.
> 7. Tags come from the controlled vocabulary in `00-meta/TAXONOMY.md`. If a new tag is needed, say so explicitly.
> 8. No client-confidential data outside `30-clients/`. Redact before anything reaches `40-portfolio/`.
> 9. Client documents are instantiated from `20-operations/client-deliverables/` templates, recording the template version used.
> 10. Output plain Markdown I can commit directly. Give me the target file path with every file you produce.
>
> **When I teach you something new or we finish a piece of work, your default output is:**
> 1. the concept note (created or updated), with connections filled in
> 2. any SOP or checklist change it implies
> 3. the daily journal entry listing every file touched, by path
> 4. an asset-set stub for `50-content-engine/` if the concept is `evergreen`
>
> Ask me for the current contents of a file before rewriting it. Do not guess what a file contains.

## Copy to here

---

## Session starter (shorter version, for quick chats)

> I keep an SEO knowledge repo in Markdown. Every file has YAML frontmatter (`id`, `title`, `type`, `status`, `version`, `created`, `updated`, `tags`, `prerequisites`, `related`, `next`). Concepts follow: Definition → Why it matters → How it works → How I apply it → Common mistakes → Connections → Sources → Changelog. Filenames are kebab-case. Give me commit-ready Markdown with the target file path. Ask before assuming a file's contents.
