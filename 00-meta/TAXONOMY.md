---
id: meta-taxonomy
title: Taxonomy — ID Prefixes and Tag Vocabulary
type: standard
status: growing
version: 1.0
created: 2026-07-25
updated: 2026-07-25
tags: [meta, system, standards]
related: [meta-documentation-standard, meta-naming-conventions]
---

# Taxonomy v1.0

The controlled vocabulary. One name per thing, forever. This is what makes search work.

---

## 1. ID prefixes

| Prefix | Domain | Lives in |
|---|---|---|
| `meta-` | System rules | `00-meta/` |
| `fund-` | SEO fundamentals | `10-knowledge/01-fundamentals/` |
| `tech-` | Technical SEO | `10-knowledge/02-technical-seo/` |
| `onpage-` | On-page SEO | `10-knowledge/03-on-page-seo/` |
| `offpage-` | Off-page, backlinks, digital PR | `10-knowledge/04-off-page-seo/` |
| `content-` | Content SEO and strategy | `10-knowledge/05-content-seo/` |
| `semantic-` | Semantic SEO, entities, knowledge graphs | `10-knowledge/06-semantic-seo/` |
| `schema-` | Structured data | `10-knowledge/07-structured-data/` |
| `aisearch-` | AEO, GEO, AI Mode, ChatGPT Search, Perplexity, Gemini | `10-knowledge/08-ai-search/` |
| `local-` | Local SEO | `10-knowledge/09-local-seo/` |
| `ecom-` | E-commerce SEO | `10-knowledge/10-ecommerce-seo/` |
| `intl-` | International SEO | `10-knowledge/11-international-seo/` |
| `enterprise-` | Enterprise SEO | `10-knowledge/12-enterprise-seo/` |
| `research-` | Keyword, competitor, entity research | `10-knowledge/13-research/` |
| `strategy-` | Topical authority, internal linking, roadmapping | `10-knowledge/14-strategy/` |
| `platform-` | Search Console, GA4, GTM, Looker Studio, Bing, etc. | `10-knowledge/15-platforms/` |
| `measure-` | Measurement, attribution, forecasting, reporting theory | `10-knowledge/16-measurement/` |
| `playbook-` | Industry playbooks | `15-business-playbooks/` |
| `sop-` | Standard operating procedures | `20-operations/` |
| `chk-` | Checklists | `20-operations/` |
| `deliv-` | Client deliverable templates | `20-operations/` |
| `sim-` | Agency simulator exercises | `20-operations/` |
| `client-` | Client workspace documents | `30-clients/` |
| `case-` | Case studies and portfolio pieces | `40-portfolio/` |
| `asset-` | Content engine assets | `50-content-engine/` |
| `jrnl-` | Daily learning entries | `60-journal/` |
| `mist-` | Mistake journal entries | `60-journal/` |
| `rev-` | Weekly and monthly reviews | `60-journal/` |
| `radar-` | Dated industry intelligence | `70-radar/` |
| `prompt-` | Prompt library | `80-library/` |
| `tool-` | Tool profiles | `80-library/` |
| `fw-` | Named frameworks | `80-library/` |
| `ref-` | External references | `80-library/` |
| `gloss-` | Glossary terms | `80-library/` |

---

## 2. Tag vocabulary

Tags are faceted. Use 2–5 per file, drawn from these lists only. Adding a tag means adding it here in the same commit.

### Domain facet
`seo-fundamentals` · `technical-seo` · `on-page-seo` · `off-page-seo` · `content-seo` · `semantic-seo` · `local-seo` · `ecommerce-seo` · `international-seo` · `enterprise-seo` · `ai-search` · `structured-data` · `analytics` · `measurement` · `strategy` · `research`

### Sub-topic facet
`crawling` · `indexing` · `rendering` · `site-architecture` · `page-speed` · `core-web-vitals` · `logs` · `canonicalisation` · `hreflang` · `javascript-seo` · `migrations` · `entities` · `knowledge-graph` · `topical-authority` · `internal-linking` · `search-intent` · `keyword-research` · `competitor-research` · `content-strategy` · `editorial` · `eeat` · `link-building` · `digital-pr` · `gbp` · `citations` · `reviews` · `aeo` · `geo` · `llm-visibility` · `serp-features` · `algorithm-updates`

### Platform facet
`google-search` · `google-ai-mode` · `ai-overviews` · `chatgpt-search` · `perplexity` · `gemini` · `bing` · `search-console` · `ga4` · `gtm` · `looker-studio` · `screaming-frog` · `ahrefs` · `semrush` · `wordpress` · `shopify` · `webflow`

### Industry facet
`law-firms` · `dentists` · `healthcare` · `saas` · `ecommerce-retail` · `real-estate` · `education` · `restaurants` · `travel` · `local-services` · `b2b` · `b2c`

### Function facet
`audit` · `reporting` · `onboarding` · `discovery` · `proposal` · `pitching` · `client-management` · `pricing` · `objection-handling` · `presentation` · `project-management` · `qa`

### System facet
`meta` · `system` · `standards` · `template` · `checklist` · `sop` · `practice` · `portfolio` · `teaching` · `mistake` · `lesson` · `review` · `news`

### Confidence facet (optional, on concepts)
`verified` — tested in real work · `theory` — read but not yet applied · `contested` — practitioners disagree · `volatile` — likely to change within a year

---

## 3. Anti-patterns

- Do not create both `backlinks` and `link-building`. One concept, one tag.
- Do not tag with the folder name. The path already says that.
- Do not use tags as a status field. `status:` exists for that.
