---
id: meta-workflows
title: Workflows — The Rituals That Keep This Alive
type: standard
status: evergreen
version: 1.0
created: 2026-07-25
updated: 2026-07-25
tags: [meta, system, review]
related: [meta-documentation-standard, meta-knowledge-map]
---

# Workflows v1.0

A repository without rituals becomes a graveyard. These are the loops that turn activity into permanent assets.

---

## 1. The Harvest Loop (daily, 15 minutes)

Every lesson, client task, video, or article becomes repository assets the same day. Nothing waits for "when I have time to write it up".

```
Something learned
      │
      ├──► 60-journal/daily/YYYY-MM-DD.md        (what happened, raw)
      │
      ├──► 10-knowledge/<domain>/<concept>.md    (concept created or updated, links declared)
      │
      ├──► 20-operations/                        (if it changed how I work → SOP or checklist)
      │
      ├──► 50-content-engine/<concept>/          (asset set stub created, 11 slots)
      │
      ├──► 80-library/                           (if it produced a prompt, tool insight, or framework)
      │
      └──► 60-journal/mistakes/                  (if something went wrong → mistake entry)
```

**Definition of done for a learning day:** the daily journal entry lists every file created or updated, by path. If the list is empty, the day produced nothing permanent.

---

## 2. Weekly Review (Sunday, 45 minutes)

Run against `00-meta/templates/weekly-review.md`.

- [ ] Read the week's daily entries
- [ ] Promote statuses: `seed` → `growing` → `evergreen`
- [ ] **Link audit:** every note created this week has `prerequisites` / `related` / `next` filled, and every link is reciprocated on the other end
- [ ] Check orphans: any note not linked from at least one folder README or hub
- [ ] Move any completed client work toward portfolio graduation
- [ ] Pick next week's learning focus and one asset to publish
- [ ] Log structural changes in `CHANGELOG.md`

---

## 3. Monthly Review (last day of month, 90 minutes)

Run against `00-meta/templates/monthly-review.md`.

- [ ] Skills audit: what can I now do that I could not last month, with evidence (file paths)
- [ ] Knowledge gaps: which domains in `10-knowledge/` are still thin
- [ ] Radar graduation: which `70-radar/` entries are now settled fact and should become concepts in `10-knowledge/`
- [ ] Deprecation sweep: what is no longer true → mark `deprecated`, move to `90-archive/`
- [ ] Template versioning: which templates changed enough to bump a MAJOR version
- [ ] Portfolio review: is there a publishable case study
- [ ] Business review: pipeline, rates, positioning

---

## 4. Client Engagement Lifecycle

```
Lead
 └─► Proposal            (20-operations deliverable template → 30-clients/<client>/01-proposal/)
      └─► Discovery      (questionnaire + call notes → 30-clients/<client>/02-discovery/)
           └─► Audit     (SOP + checklist → deliverable → 03-audits/)
                └─► Strategy   (keyword research, topical map, roadmap → 04-strategy/)
                     └─► Delivery loop   (monthly: work → report → presentation → 05-reporting/)
                          └─► Engagement close
                               ├─► Portfolio graduation (40-portfolio/)
                               ├─► SOP improvements (20-operations/)
                               ├─► Lessons + mistakes (60-journal/)
                               └─► Archive (90-archive/clients/)
```

**Rule:** client work never invents a document. It instantiates a template from `20-operations/client-deliverables/` and records the template version used. If a template was missing, creating it is part of the job.

---

## 5. Portfolio Graduation

A project becomes portfolio-ready by process, not by scramble before an interview.

1. Copy `00-meta/templates/case-study.md` into `40-portfolio/case-studies/`
2. Pull results from the client's reporting folder
3. **Redact:** apply the redaction rules in `40-portfolio/README.md` — anonymise the client if there is no written permission, convert absolute revenue to percentages, remove URLs of unlaunched work
4. Extract 2–3 portfolio samples (the actual deliverables, sanitised) into `40-portfolio/samples/`
5. Write the one-page version for a CV or pitch deck
6. Link the case study back to the concepts, SOPs, and playbooks it exercised

---

## 6. Content Multiplication

Every `evergreen` concept earns an asset set in `50-content-engine/`. One concept, eleven outputs, produced from the same source note so the message never contradicts itself. See `50-content-engine/README.md` for the pipeline and `00-meta/templates/content-asset-set.md` for the kit.

---

## 7. Radar Graduation

`70-radar/` holds dated, possibly-temporary intelligence. When something has held true for 60+ days and I have applied it in real work, it graduates: a concept in `10-knowledge/` is created or updated, and the radar entry links forward to it. This keeps the encyclopedia stable and the news log honest.

---

## 8. Practice Loop (Agency Simulator)

When there is no live client, `20-operations/agency-simulator/` supplies the work: a mock job posting, a fake client, a real website to audit. Every simulation produces the same deliverables as paid work, gets reviewed against the same checklists, and can graduate to `40-portfolio/` clearly labelled as a self-directed project. Practice is never labelled as client work.
