---
id: meta-templates-index
title: Template Library
type: hub
status: evergreen
version: 1.0
created: 2026-07-25
updated: 2026-07-25
tags: [meta, system, template]
related: [meta-documentation-standard]
---

# Template Library v1.0

**No file in this repository is created from scratch.** Copy the matching template, fill it in, delete the instruction comments.

| Template | Use for | Goes to |
|---|---|---|
| [concept.md](./concept.md) | Any SEO concept, the encyclopedia entry | `10-knowledge/` |
| [hub-readme.md](./hub-readme.md) | A folder's index page | any folder |
| [sop.md](./sop.md) | A repeatable process | `20-operations/sops/` |
| [checklist.md](./checklist.md) | Pure verification, binary items | `20-operations/checklists/` |
| [framework.md](./framework.md) | A named model or decision structure | `80-library/frameworks/` |
| [business-playbook.md](./business-playbook.md) | An industry playbook | `15-business-playbooks/` |
| [client-deliverable.md](./client-deliverable.md) | Any document sent to a client | `20-operations/client-deliverables/` |
| [client-workspace-readme.md](./client-workspace-readme.md) | A new client's workspace index | `30-clients/<client>/` |
| [meeting-notes.md](./meeting-notes.md) | Any client or internal call | `30-clients/<client>/` |
| [case-study.md](./case-study.md) | A completed project, portfolio-ready | `40-portfolio/case-studies/` |
| [portfolio-sample.md](./portfolio-sample.md) | A sanitised deliverable used as proof of skill | `40-portfolio/samples/` |
| [content-asset-set.md](./content-asset-set.md) | The 11-format multiplication kit for one concept | `50-content-engine/` |
| [daily-journal.md](./daily-journal.md) | Daily learning entry | `60-journal/daily/` |
| [mistake-entry.md](./mistake-entry.md) | Something that went wrong | `60-journal/mistakes/` |
| [weekly-review.md](./weekly-review.md) | Weekly review | `60-journal/weekly/` |
| [monthly-review.md](./monthly-review.md) | Monthly review | `60-journal/monthly/` |
| [radar-entry.md](./radar-entry.md) | An update, announcement, or observed change | `70-radar/` |
| [prompt.md](./prompt.md) | A reusable AI prompt | `80-library/prompts/` |
| [tool-profile.md](./tool-profile.md) | A tool I use | `80-library/tools/` |
| [glossary-term.md](./glossary-term.md) | A term definition | `80-library/glossary/` |
| [simulation-brief.md](./simulation-brief.md) | A practice exercise | `20-operations/agency-simulator/` |

## Conventions inside templates

- `{{PLACEHOLDER}}` — replace with real content.
- `<!-- instruction -->` — guidance for me. Delete before committing, and always before sending to a client.
- Every template's own `version` is tracked. When you improve a template, bump it and note it in `00-meta/CHANGELOG.md`.
