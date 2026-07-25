---
id: meta-index
title: 00-meta — The Rules of the System
type: hub
status: evergreen
version: 1.0
created: 2026-07-25
updated: 2026-07-25
tags: [meta, system]
---

# 00-meta

This folder is the operating manual for the repository. It contains no SEO knowledge. It contains the rules that keep the SEO knowledge consistent, linked, and findable for years.

**If you only read one file here, read [DOCUMENTATION-STANDARD.md](./DOCUMENTATION-STANDARD.md).**

## Contents

| File | Purpose | Read when |
|---|---|---|
| [DOCUMENTATION-STANDARD.md](./DOCUMENTATION-STANDARD.md) | Frontmatter spec, body structure, status lifecycle, versioning | Before creating or editing any file |
| [NAMING-CONVENTIONS.md](./NAMING-CONVENTIONS.md) | File names, folder names, ID format, link syntax | Before creating a new file |
| [TAXONOMY.md](./TAXONOMY.md) | The controlled vocabulary: ID prefixes and every allowed tag | When tagging a note |
| [WORKFLOWS.md](./WORKFLOWS.md) | The rituals: daily harvest, weekly review, client lifecycle, portfolio graduation | Daily |
| [KNOWLEDGE-MAP.md](./KNOWLEDGE-MAP.md) | The master map of concept chains across all domains | When placing a new concept |
| [templates/](./templates/) | One template per note type. Copy, never invent | Every time you create a file |
| [ROADMAP.md](./ROADMAP.md) | What is built, what is next | Weekly |
| [CHANGELOG.md](./CHANGELOG.md) | Structural changes to the repository itself | When changing the system |
| [AGENT-BRIEFING.md](./AGENT-BRIEFING.md) | Paste-into-any-AI primer on this repository | Starting a new AI session |

## Why this folder exists

Second brains do not fail from lack of content. They fail from inconsistency: three formats for the same note type, four names for the same tag, links that point nowhere. By month six nothing is findable and the repo is abandoned.

This folder is the defence against that. It costs ten minutes to consult and saves the entire system.

## Rule for changing the system

Changes to the standard, taxonomy, or folder structure are **versioned and logged** in [CHANGELOG.md](./CHANGELOG.md). Retroactive migration is optional; new files must follow the current version. Never silently change a rule.
