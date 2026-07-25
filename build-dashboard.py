#!/usr/bin/env python3
"""
build-dashboard.py — generates index.html, the interactive control panel for SEO Brain.

Run from the repository root:

    python3 tools/build-dashboard.py

Reads the real files in this repository (templates, folder READMEs, agent briefing)
and writes a single self-contained index.html with no build step and no dependencies
beyond a webfont link. Re-run it whenever the repository structure changes.

Requires nothing but Python 3.8+.
"""

import json
import os
import re
import sys
from datetime import date

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Branch used to build GitHub links. Change if your default branch is not main.
BRANCH = "main"

# ---------------------------------------------------------------------------
# 1. Folder registry
# ---------------------------------------------------------------------------

FOLDERS = [
    ("00-meta", "The rules of the system",
     "Documentation standard, naming conventions, taxonomy, workflows, master knowledge map, agent briefing, and the full template library. No SEO knowledge lives here — only the rules that keep the SEO knowledge consistent and findable."),
    ("10-knowledge", "The encyclopedia",
     "Evergreen concepts. No dates, no client names, no tactic-of-the-month. 16 domain folders, each with its own concept chain. This is what a career could be rebuilt from."),
    ("15-business-playbooks", "Industry playbooks",
     "What is different per vertical: search behaviour, strategy, keyword landscape, entities, topical maps, content strategy, local considerations, AEO/GEO opportunities, realistic KPIs. Each carries an evidence log that grows from theory into tested knowledge."),
    ("20-operations", "How work gets done",
     "SOPs, binary checklists, a client deliverable template for every document a client ever receives, an agency simulator for practice projects, and internal ops (pricing, scoping, QA)."),
    ("30-clients", "Client workspaces",
     "One folder per client with a fixed nine-folder shape. Client work instantiates templates and records the version used. Credentials are never stored — only a note of where access lives."),
    ("40-portfolio", "Proof of skill",
     "Case studies, sanitised deliverable samples, one-pagers, redaction rules, and a skills matrix mapping each case study to the concepts it proves. Client work and self-directed projects are always labelled distinctly."),
    ("50-content-engine", "Knowledge into content",
     "Every evergreen concept becomes eleven assets, all derived from one source note so the message never contradicts itself. When the source changes, its assets are flagged stale."),
    ("60-journal", "The record",
     "Dated and append-only: daily learning, mistakes, weekly and monthly reviews. Every mistake entry ends with a systemic fix, so the error is prevented by a checklist rather than by memory."),
    ("70-radar", "Industry intelligence",
     "Dated, possibly-temporary knowledge, kept out of the encyclopedia so it stays stable. Every entry separates confirmed from inferred. Held true 60+ days and applied in real work? It graduates into 10-knowledge."),
    ("80-library", "Reusable inputs",
     "Prompts, tool profiles, named frameworks, external references, glossary, and benchmark data."),
    ("90-archive", "Nothing is deleted",
     "Deprecated tactics, retired SOPs, superseded template versions, closed engagements. Every archived file states why it was retired and what replaced it."),
]

# ---------------------------------------------------------------------------
# 2. Curriculum: the 13 chains. "Node|folder-override" pins a node's home.
# ---------------------------------------------------------------------------

CHAINS = [
    ("How search engines work", "10-knowledge/02-technical-seo", [
        "Search Fundamentals|10-knowledge/01-fundamentals", "Crawling", "Robots.txt", "Crawl Budget",
        "XML Sitemaps", "Rendering", "Indexing", "Canonicalisation",
        "Ranking Systems|10-knowledge/01-fundamentals", "SERP Features|10-knowledge/01-fundamentals",
    ]),
    ("Site architecture", "10-knowledge/02-technical-seo", [
        "Site Architecture", "URL Structure", "Internal Linking|10-knowledge/14-strategy",
        "Crawl Depth", "Pagination and Faceted Navigation", "Log File Analysis",
    ]),
    ("Meaning and entities", "10-knowledge/06-semantic-seo", [
        "Entities", "Entity Salience", "Structured Data|10-knowledge/07-structured-data",
        "Knowledge Graph", "Semantic Search", "Topical Authority|10-knowledge/14-strategy",
        "AI Search Visibility|10-knowledge/08-ai-search",
    ]),
    ("Research to strategy", "10-knowledge/13-research", [
        "Keyword Research", "Search Intent", "SERP Analysis", "Competitor Research",
        "Entity Research", "Topical Maps|10-knowledge/14-strategy",
        "Content Strategy|10-knowledge/05-content-seo", "Editorial Calendar|10-knowledge/05-content-seo",
    ]),
    ("Content and quality", "10-knowledge/05-content-seo", [
        "Content Types", "Search Intent Matching", "On-Page Optimisation|10-knowledge/03-on-page-seo",
        "E-E-A-T", "Content Refresh", "Content Pruning", "Cannibalisation",
    ]),
    ("Authority", "10-knowledge/04-off-page-seo", [
        "Links as Signals", "Link Quality", "Anchor Text", "Digital PR",
        "Link Prospecting", "Outreach", "Link Risk and Disavow", "Brand Signals",
    ]),
    ("AI search", "10-knowledge/08-ai-search", [
        "AI Search Landscape", "How LLMs Retrieve", "AEO", "GEO",
        "Google AI Mode and AI Overviews", "ChatGPT Search", "Perplexity", "Gemini",
        "LLM Visibility Measurement",
    ]),
    ("Local", "10-knowledge/09-local-seo", [
        "Local Ranking Factors", "Google Business Profile", "NAP and Citations", "Reviews",
        "Local Landing Pages", "Multi-Location", "Local Link Building",
    ]),
    ("E-commerce", "10-knowledge/10-ecommerce-seo", [
        "E-commerce Architecture", "Category Pages", "Product Pages", "Faceted Navigation",
        "Product Schema", "Feed Optimisation", "Seasonality", "Merchandising and SEO",
    ]),
    ("International", "10-knowledge/11-international-seo", [
        "International Strategy", "ccTLD vs Subfolder", "Hreflang", "Content Localisation",
        "Currency and Market Signals", "International Crawl Management",
    ]),
    ("Enterprise", "10-knowledge/12-enterprise-seo", [
        "Enterprise Constraints", "Stakeholder Management", "Prioritisation Frameworks",
        "SEO in the Dev Cycle", "Platform Migrations", "Governance at Scale",
        "Automation and Internal Tooling",
    ]),
    ("Measurement", "10-knowledge/16-measurement", [
        "Measurement Fundamentals", "Search Console|10-knowledge/15-platforms",
        "GA4|10-knowledge/15-platforms", "Tag Manager|10-knowledge/15-platforms",
        "Looker Studio|10-knowledge/15-platforms", "KPI Design", "Forecasting",
        "Attribution", "Client Reporting",
    ]),
    ("Commercial craft", "20-operations/internal-ops", [
        "Positioning and Niche", "Lead Generation", "Discovery Calls", "Proposals and Pricing",
        "Onboarding", "Client Communication", "Objection Handling", "Retention and Upsell",
        "Case Studies",
    ]),
]

BRIDGES = [
    ("Internal Linking ↔ Crawl Budget ↔ Topical Authority", "One tactic serving three different goals"),
    ("Entities ↔ Keyword Research", "Modern research is entity-first, not string-first"),
    ("Structured Data ↔ AI Search ↔ Local SEO", "Schema is the shared substrate"),
    ("Search Intent ↔ Content Strategy ↔ Reporting KPIs", "Intent decides what success even means"),
    ("Architecture ↔ Faceted Navigation ↔ Enterprise Governance", "The same problem at three scales"),
    ("Every chain ↔ Business playbooks", "Where general theory becomes an industry plan"),
    ("Every concept ↔ Operations", "A concept with no SOP is not yet operational"),
]

PLAYBOOKS = [
    ("Law firms", "law-firms", "High value per case, trust-driven, heavily regulated advertising rules"),
    ("Dentists", "dentists", "Local pack decides everything; reviews and treatment pages carry the revenue"),
    ("Healthcare", "healthcare", "E-E-A-T is not optional; author credentials and review process are ranking infrastructure"),
    ("SaaS", "saas", "Topical authority plus product-led content; long sales cycles blur attribution"),
    ("E-commerce", "ecommerce", "Architecture, faceted navigation, feeds and seasonality outrank content strategy"),
    ("Real estate", "real-estate", "Inventory churn and programmatic pages against portal dominance"),
    ("Education", "education", "Long consideration cycles, intake seasonality, credential-led trust signals"),
    ("Restaurants", "restaurants", "Near-zero research phase; profile completeness and photos beat blogs"),
    ("Travel", "travel", "Extreme seasonality, aggregator competition, itinerary and destination clusters"),
    ("Local businesses", "local-businesses", "Proximity, categories and citation consistency over content volume"),
]

PLAYBOOK_SECTIONS = [
    "Market and business model", "Search behaviour", "SEO strategy", "Keyword landscape",
    "Entities", "Topical map", "Content strategy", "Local SEO considerations",
    "AEO / GEO opportunities", "KPIs", "Client objections", "Vertical-tuned deliverables",
]

CONTENT_FORMATS = [
    ("Long-form YouTube script", "Depth, evergreen search traffic, authority"),
    ("Short YouTube script", "One idea, one payoff, under 60 seconds"),
    ("Reel series", "Three to five reels from one concept, each with its own hook"),
    ("Carousel", "Instagram and LinkedIn; the diagram does the work"),
    ("LinkedIn post", "Practitioner credibility, client-facing proof"),
    ("Blog article", "The searchable home of the concept"),
    ("Newsletter", "Direct audience, no algorithm between you and them"),
    ("Course notes", "Student-facing, sequential, assessable"),
    ("Teaching notes", "My delivery notes: the analogies, the questions to ask, the timing"),
    ("Voice-over script", "Written to be spoken, not read"),
    ("Product-ready documentation", "Reference form; the version a client or team member uses"),
]

DELIVERABLES = [
    "Proposal", "Discovery questionnaire", "Audit report", "Keyword research",
    "Technical audit", "Content strategy", "Monthly report", "Client presentation",
    "Email templates", "Meeting notes", "SOPs", "Checklists",
]

SIMULATIONS = [
    ("Mock job postings", "Reverse-engineer a real job ad into a skills gap list, then close one gap"),
    ("Client onboarding simulations", "Full onboarding against a fictional client with a hidden constraint"),
    ("Discovery calls", "Practise the questions that reveal the unstated real goal"),
    ("Practice websites", "Real sites, audited as if paid for"),
    ("Technical audits", "Same SOP, same checklist, same deliverable as client work"),
    ("SEO reports", "Report on a site you do not control, with honest attribution"),
    ("Client objections", "Rehearse the answer to \u201cwhy is this taking so long\u201d before hearing it live"),
    ("Reporting exercises", "Turn raw data into one page an owner will actually read"),
    ("Portfolio projects", "Self-directed work, always labelled as such"),
    ("Review checklists", "Score your own work the way a senior strategist would"),
]

WEEKLY = [
    "Read the week's daily entries",
    "Promote statuses: seed to growing to evergreen",
    "Every new note has prerequisites, related and next filled in",
    "Every link is reciprocated on the other end",
    "Every new note is reachable from a folder README",
    "No orphan files, no placeholders left in committed files",
    "Client work moved toward portfolio graduation",
    "Next week's learning focus chosen",
    "One asset picked to publish",
    "CHANGELOG updated if the system changed",
]

MONTHLY = [
    "Capability audit with file-path evidence",
    "Knowledge gap count per domain chain",
    "Radar graduation: entries true for 60+ days and applied",
    "Deprecation sweep: what is no longer true",
    "Template and SOP version bumps",
    "Portfolio review: is it strong enough for the work I want",
    "Business review: leads, proposals, retainers, effective rate",
    "Repeated mistakes: which process changes, not which resolve",
]

HARVEST = [
    ("Daily journal", "60-journal/daily/YYYY-MM-DD.md", "Raw capture of what happened"),
    ("Concept note", "10-knowledge/", "Created or updated, connections declared"),
    ("Operations", "20-operations/", "If it changed how I work: SOP or checklist"),
    ("Asset set", "50-content-engine/", "Stub created if the concept is evergreen"),
    ("Library", "80-library/", "Any prompt, tool insight or framework produced"),
    ("Mistakes", "60-journal/mistakes/", "If something went wrong, with a systemic fix"),
]

FRONTMATTER = [
    ("id", "Permanent, kebab-case, domain prefix", "Never changes. Titles may change, ids never"),
    ("title", "Human title, Title Case", ""),
    ("type", "concept, sop, checklist, template, playbook…", "21 allowed values"),
    ("status", "seed, growing, evergreen, deprecated", "Promotion is deliberate, reviewed weekly"),
    ("version", "MAJOR.MINOR", "Required on templates, SOPs, checklists, deliverables"),
    ("created", "ISO 8601", "Never changes"),
    ("updated", "ISO 8601", "Bumped on every meaningful edit"),
    ("tags", "2–5, from the controlled vocabulary", "New tag means updating the taxonomy in the same commit"),
    ("prerequisites", "ids — what to understand first", "The up direction"),
    ("related", "ids — sideways connections", "Must be reciprocated on the other end"),
    ("next", "ids — what this unlocks", "The forward direction"),
    ("sources", "URLs or citations", "Omit if empty rather than carrying an empty list"),
]

STATUSES = [
    ("seed", "Captured, incomplete, may be wrong", "Fine to be rough. Must still have frontmatter"),
    ("growing", "Being developed and tested in real work", "Definition and mechanics are correct"),
    ("evergreen", "I can teach it and defend it to a client", "Complete, linked, no known gaps"),
    ("deprecated", "No longer true or no longer used", "States why, links to what replaced it, moves to archive"),
]

RULES = [
    "One canonical location per asset. Never duplicate, always link.",
    "Links are declared on both ends, or the map has one-way streets.",
    "Filenames are kebab-case.md, no dates — except journal and radar, named YYYY-MM-DD.md.",
    "Every folder has a README.md acting as its hub and index.",
    "No file is created from scratch. Copy from the template library.",
    "Nothing is deleted. It is deprecated and archived, with a reason.",
    "No client-confidential data outside 30-clients. Redact before the portfolio.",
    "Client documents record the template version that produced them.",
]


# ---------------------------------------------------------------------------
# 3. Read the repository
# ---------------------------------------------------------------------------

def read(path):
    full = os.path.join(ROOT, path)
    if not os.path.exists(full):
        return None
    with open(full, encoding="utf-8") as fh:
        return fh.read()


def frontmatter_value(text, key):
    m = re.search(r"^%s:\s*(.+)$" % key, text, re.M)
    return m.group(1).strip() if m else ""


def load_templates():
    tdir = os.path.join(ROOT, "00-meta", "templates")
    out = []
    if not os.path.isdir(tdir):
        return out
    for name in sorted(os.listdir(tdir)):
        if not name.endswith(".md") or name == "README.md":
            continue
        text = read("00-meta/templates/" + name)
        out.append({
            "file": name,
            "path": "00-meta/templates/" + name,
            "title": frontmatter_value(text, "title") or name,
            "type": frontmatter_value(text, "type"),
            "version": frontmatter_value(text, "version"),
            "lines": len(text.splitlines()),
            "body": text,
        })
    return out


def load_briefing():
    text = read("00-meta/AGENT-BRIEFING.md") or ""
    m = re.search(r"## Copy from here down\s*(.*?)\s*## Copy to here", text, re.S)
    if not m:
        return ""
    block = m.group(1)
    lines = []
    for line in block.splitlines():
        line = re.sub(r"^>\s?", "", line)
        lines.append(line)
    return "\n".join(lines).strip()


def count_files():
    counts = {}
    for folder, _, _ in FOLDERS:
        n = 0
        for _root, _dirs, files in os.walk(os.path.join(ROOT, folder)):
            n += len([f for f in files if f.endswith(".md")])
        counts[folder] = n
    return counts


def exists(path):
    return os.path.exists(os.path.join(ROOT, path))


def build_payload():
    counts = count_files()
    chains = []
    for i, (name, home, nodes) in enumerate(CHAINS, start=1):
        parsed = []
        for n in nodes:
            if "|" in n:
                title, folder = n.split("|", 1)
            else:
                title, folder = n, home
            slug = re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-")
            path = "%s/%s.md" % (folder, slug)
            parsed.append({
                "id": "%s/%s" % (folder, slug),
                "title": title,
                "path": path,
                "exists": exists(path),
            })
        chains.append({"n": i, "name": name, "home": home, "nodes": parsed})

    return {
        "generated": date.today().isoformat(),
        "branch": BRANCH,
        "folders": [{"path": f, "tagline": t, "purpose": p, "files": counts.get(f, 0),
                     "exists": exists(f + "/README.md")}
                    for f, t, p in FOLDERS],
        "chains": chains,
        "bridges": [{"pair": a, "why": b} for a, b in BRIDGES],
        "playbooks": [{"name": n, "slug": s, "note": w,
                       "exists": exists("15-business-playbooks/%s.md" % s)} for n, s, w in PLAYBOOKS],
        "playbookSections": PLAYBOOK_SECTIONS,
        "formats": [{"name": n, "job": j} for n, j in CONTENT_FORMATS],
        "deliverables": DELIVERABLES,
        "simulations": [{"name": n, "note": w} for n, w in SIMULATIONS],
        "weekly": WEEKLY,
        "monthly": MONTHLY,
        "harvest": [{"stage": a, "path": b, "note": c} for a, b, c in HARVEST],
        "frontmatter": [{"field": a, "value": b, "note": c} for a, b, c in FRONTMATTER],
        "statuses": [{"status": a, "meaning": b, "bar": c} for a, b, c in STATUSES],
        "rules": RULES,
        "templates": load_templates(),
        "briefing": load_briefing(),
    }


# ---------------------------------------------------------------------------
# 4. The page
# ---------------------------------------------------------------------------

CSS = r"""
*,*::before,*::after{box-sizing:border-box}
:root{
  --ink:#131A22; --ink-2:#3D4A57; --ink-3:#6B7885;
  --paper:#E7EBEE; --panel:#FFFFFF; --panel-2:#F4F6F8;
  --rule:#C9D2DA; --rule-2:#E1E7EC;
  --link:#1B4F9C;
  --seed:#8C98A8; --growing:#C08320; --evergreen:#2E7D5B; --deprecated:#A34B3C;
  --shadow:0 1px 2px rgba(19,26,34,.06),0 8px 24px -16px rgba(19,26,34,.28);
  --mono:"IBM Plex Mono",ui-monospace,SFMono-Regular,Menlo,monospace;
  --sans:"IBM Plex Sans",-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif;
  --display:"Space Grotesk","IBM Plex Sans",sans-serif;
}
html{-webkit-text-size-adjust:100%}
body{margin:0;background:var(--paper);color:var(--ink);font-family:var(--sans);
  font-size:15px;line-height:1.6;-webkit-font-smoothing:antialiased}
a{color:var(--link);text-decoration:none;border-bottom:1px solid rgba(27,79,156,.28)}
a:hover{border-bottom-color:var(--link)}
h1,h2,h3,h4{font-family:var(--display);font-weight:600;letter-spacing:-.01em;line-height:1.2;margin:0}
code,kbd{font-family:var(--mono);font-size:.86em}
:focus-visible{outline:2px solid var(--link);outline-offset:2px;border-radius:2px}

/* shell */
.shell{display:grid;grid-template-columns:250px minmax(0,1fr);min-height:100vh}
.rail{background:var(--ink);color:#DCE3EA;padding:22px 0 40px;position:sticky;top:0;height:100vh;overflow-y:auto}
.brand{padding:0 20px 18px;border-bottom:1px solid rgba(255,255,255,.1);margin-bottom:14px}
.brand h1{font-size:19px;color:#fff;letter-spacing:-.02em}
.brand p{margin:6px 0 0;font-family:var(--mono);font-size:10.5px;letter-spacing:.08em;
  text-transform:uppercase;color:#7D8B99}
.nav{display:flex;flex-direction:column;gap:1px;padding:0 8px}
.nav button{all:unset;cursor:pointer;display:flex;gap:10px;align-items:baseline;
  padding:8px 12px;border-radius:5px;font-size:13.5px;color:#B9C4CE}
.nav button .num{font-family:var(--mono);font-size:10.5px;color:#6E7C8A;min-width:20px}
.nav button:hover{background:rgba(255,255,255,.06);color:#fff}
.nav button[aria-current="true"]{background:#F4F6F8;color:var(--ink);font-weight:500}
.nav button[aria-current="true"] .num{color:var(--ink-3)}
.rail-foot{padding:20px 20px 0;margin-top:20px;border-top:1px solid rgba(255,255,255,.1);
  font-size:11.5px;color:#7D8B99;line-height:1.5}
.rail-foot code{color:#AEBAC6;font-size:11px}

main{padding:0 0 80px;min-width:0}
.topbar{position:sticky;top:0;z-index:20;background:rgba(231,235,238,.9);
  backdrop-filter:blur(8px);border-bottom:1px solid var(--rule);
  padding:12px 32px;display:flex;gap:14px;align-items:center;flex-wrap:wrap}
.search{flex:1 1 240px;display:flex;align-items:center;gap:8px;background:var(--panel);
  border:1px solid var(--rule);border-radius:6px;padding:7px 11px;min-width:0}
.search input{all:unset;flex:1;font-family:var(--sans);font-size:14px;min-width:0;color:var(--ink)}
.search .hint{font-family:var(--mono);font-size:10px;color:var(--ink-3);
  border:1px solid var(--rule);border-radius:3px;padding:1px 5px}
.wrap{padding:34px 32px 0;max-width:1000px}
.eyebrow{font-family:var(--mono);font-size:10.5px;letter-spacing:.12em;text-transform:uppercase;
  color:var(--ink-3);margin:0 0 10px}
.lede{font-size:16.5px;color:var(--ink-2);max-width:64ch;margin:12px 0 0}
section[hidden]{display:none}
.sec-h{margin-bottom:26px}
.sec-h h2{font-size:27px}

/* panels */
.panel{background:var(--panel);border:1px solid var(--rule);border-radius:9px;
  box-shadow:var(--shadow);padding:22px;margin:22px 0}
.panel > h3{font-size:16px;margin-bottom:4px}
.panel .sub{font-size:13px;color:var(--ink-3);margin:0 0 16px}
.grid{display:grid;gap:14px}
.g2{grid-template-columns:repeat(auto-fit,minmax(280px,1fr))}
.g3{grid-template-columns:repeat(auto-fit,minmax(210px,1fr))}

/* master map — the signature */
.map{margin:26px 0 0;background:var(--panel);border:1px solid var(--rule);border-radius:9px;
  box-shadow:var(--shadow);overflow:hidden}
.map-head{display:flex;justify-content:space-between;align-items:flex-end;gap:16px;
  padding:20px 22px 16px;border-bottom:1px solid var(--rule-2);flex-wrap:wrap}
.map-head h3{font-size:16px}
.map-head p{margin:5px 0 0;font-size:13px;color:var(--ink-3);max-width:52ch}
.coverage{text-align:right;font-family:var(--mono)}
.coverage b{display:block;font-size:30px;font-weight:500;letter-spacing:-.02em;line-height:1}
.coverage span{font-size:10.5px;letter-spacing:.1em;text-transform:uppercase;color:var(--ink-3)}
.chain-row{display:grid;grid-template-columns:26px minmax(120px,1.1fr) minmax(150px,2fr) 46px;
  gap:14px;align-items:center;width:100%;padding:11px 22px;border:0;background:none;
  border-top:1px solid var(--rule-2);cursor:pointer;text-align:left;font:inherit;color:inherit}
.chain-row:first-of-type{border-top:0}
.chain-row:hover{background:var(--panel-2)}
.chain-row .cn{font-family:var(--mono);font-size:11px;color:var(--ink-3)}
.chain-row .cname{font-size:14px;font-weight:500}
.dots{display:flex;gap:4px;flex-wrap:wrap}
.dot{width:10px;height:10px;border-radius:50%;background:var(--rule);
  border:1px solid #B9C3CC;flex:0 0 auto}
.dot.on{background:var(--evergreen);border-color:var(--evergreen)}
.pct{font-family:var(--mono);font-size:12px;color:var(--ink-2);text-align:right}

/* chain detail */
.chain-card{background:var(--panel);border:1px solid var(--rule);border-radius:9px;
  box-shadow:var(--shadow);padding:20px;margin:16px 0}
.chain-card header{display:flex;justify-content:space-between;gap:12px;align-items:baseline;
  padding-bottom:12px;border-bottom:1px solid var(--rule-2);margin-bottom:6px;flex-wrap:wrap}
.chain-card h3{font-size:16px}
.chain-card .home{font-family:var(--mono);font-size:11.5px;color:var(--ink-3)}
.ladder{list-style:none;margin:0;padding:0}
.node{display:flex;gap:12px;align-items:flex-start;padding:9px 0;position:relative}
.node:not(:last-child)::after{content:"";position:absolute;left:9px;top:28px;bottom:-2px;
  width:1px;background:var(--rule)}
.node .tick{all:unset;cursor:pointer;width:19px;height:19px;border:1.5px solid #A9B4BF;
  border-radius:50%;flex:0 0 auto;margin-top:2px;background:var(--panel);
  display:grid;place-items:center;position:relative;z-index:1}
.node .tick:hover{border-color:var(--evergreen)}
.node.done .tick{background:var(--evergreen);border-color:var(--evergreen)}
.node .tick svg{width:10px;height:10px;opacity:0}
.node.done .tick svg{opacity:1}
.node .body{min-width:0}
.node .t{font-size:14px}
.node.done .t{color:var(--ink-3)}
.node .p{font-family:var(--mono);font-size:11px;color:var(--ink-3);word-break:break-all}
.node .p a{border-bottom-color:transparent}
a.tocreate{color:var(--ink-3);border-bottom:1px dashed var(--rule)}
a.tocreate:hover{color:var(--growing);border-bottom-color:var(--growing)}
a.tocreate:hover::after{content:" · create";color:var(--growing)}

/* tables */
table{width:100%;border-collapse:collapse;font-size:13.5px}
th{text-align:left;font-family:var(--mono);font-size:10.5px;letter-spacing:.08em;
  text-transform:uppercase;color:var(--ink-3);font-weight:400;
  padding:0 12px 8px 0;border-bottom:1px solid var(--rule)}
td{padding:9px 12px 9px 0;border-bottom:1px solid var(--rule-2);vertical-align:top}
tr:last-child td{border-bottom:0}
td code{background:var(--panel-2);padding:1px 5px;border-radius:3px}

/* folder cards */
.fcard{background:var(--panel);border:1px solid var(--rule);border-radius:9px;padding:17px;
  box-shadow:var(--shadow)}
.fcard .fp{font-family:var(--mono);font-size:12px;color:var(--link);display:block;margin-bottom:3px}
.fcard h4{font-size:14.5px;margin-bottom:7px}
.fcard p{margin:0;font-size:13px;color:var(--ink-2)}
.fcard .n{font-family:var(--mono);font-size:10.5px;color:var(--ink-3);
  margin-top:11px;padding-top:9px;border-top:1px solid var(--rule-2)}

/* pills + status legend */
.pill{display:inline-flex;align-items:center;gap:6px;font-family:var(--mono);font-size:11px;
  border:1px solid var(--rule);border-radius:20px;padding:3px 10px;color:var(--ink-2);
  background:var(--panel)}
.pill i{width:7px;height:7px;border-radius:50%;background:var(--seed);display:block}
.pill.growing i{background:var(--growing)} .pill.evergreen i{background:var(--evergreen)}
.pill.deprecated i{background:var(--deprecated)}
.pills{display:flex;gap:8px;flex-wrap:wrap;margin:14px 0 0}

/* code + copy */
.copybar{display:flex;justify-content:space-between;align-items:center;gap:12px;
  border-bottom:1px solid var(--rule-2);padding-bottom:10px;margin-bottom:12px;flex-wrap:wrap}
.act{all:unset;cursor:pointer;font-family:var(--mono);font-size:11.5px;
  border:1px solid var(--rule);border-radius:5px;padding:6px 11px;background:var(--panel-2);
  color:var(--ink);white-space:nowrap;display:inline-block}
.act:hover{background:var(--ink);color:#fff;border-color:var(--ink)}
.act.on{background:var(--evergreen);border-color:var(--evergreen);color:#fff}
pre{margin:0;background:#0F1620;color:#D7DEE6;border-radius:7px;padding:16px;overflow:auto;
  font-family:var(--mono);font-size:12px;line-height:1.6;max-height:420px}
pre::-webkit-scrollbar{height:9px;width:9px}
pre::-webkit-scrollbar-thumb{background:#3A4653;border-radius:9px}

/* template list */
.tlist{display:grid;gap:10px}
.titem{background:var(--panel);border:1px solid var(--rule);border-radius:8px;overflow:hidden}
.titem > summary{cursor:pointer;padding:13px 16px;display:grid;
  grid-template-columns:minmax(0,1fr) auto;gap:12px;align-items:center;list-style:none}
.titem > summary::-webkit-details-marker{display:none}
.titem[open] > summary{border-bottom:1px solid var(--rule-2);background:var(--panel-2)}
.titem summary:hover{background:var(--panel-2)}
.titem .tt{font-size:14px;font-weight:500}
.titem .tm{font-family:var(--mono);font-size:11px;color:var(--ink-3);margin-top:2px}
.titem .tbody{padding:14px 16px 16px}

/* checklists */
.chk{list-style:none;margin:0;padding:0}
.chk li{display:flex;gap:11px;align-items:flex-start;padding:8px 0;
  border-bottom:1px solid var(--rule-2);font-size:13.5px}
.chk li:last-child{border-bottom:0}
.chk input{margin:4px 0 0;accent-color:var(--evergreen);width:16px;height:16px;flex:0 0 auto}
.chk li.done label{color:var(--ink-3);text-decoration:line-through;text-decoration-thickness:1px}

/* repo link setting */
.repo{display:flex;gap:9px;align-items:center;flex-wrap:wrap;margin-top:14px}
.repo input{font-family:var(--mono);font-size:12px;padding:7px 10px;border:1px solid var(--rule);
  border-radius:5px;background:var(--panel);min-width:min(340px,100%);color:var(--ink)}
.note{font-size:12.5px;color:var(--ink-3);margin:10px 0 0}

/* search results */
.results{display:grid;gap:8px}
.result{background:var(--panel);border:1px solid var(--rule);border-radius:7px;padding:12px 14px;
  display:grid;grid-template-columns:minmax(0,1fr) auto;gap:12px;align-items:center;
  cursor:pointer;text-align:left;font:inherit;color:inherit;width:100%}
.result:hover{border-color:var(--ink-3)}
.result .rt{font-size:14px}
.result .rk{font-family:var(--mono);font-size:10.5px;letter-spacing:.06em;text-transform:uppercase;
  color:var(--ink-3)}
.empty{padding:30px;text-align:center;color:var(--ink-3);font-size:14px;
  border:1px dashed var(--rule);border-radius:9px}

@media (max-width:860px){
  .shell{grid-template-columns:1fr}
  .rail{position:static;height:auto;padding-bottom:18px}
  .nav{flex-direction:row;overflow-x:auto;gap:4px;padding:0 12px 4px}
  .nav button{white-space:nowrap}
  .nav button .num{display:none}
  .rail-foot{display:none}
  .topbar,.wrap{padding-left:18px;padding-right:18px}
  .chain-row{grid-template-columns:20px minmax(90px,1fr) 40px;gap:10px}
  .chain-row .dots{display:none}
}
@media (prefers-reduced-motion:no-preference){
  .panel,.fcard,.chain-card,.map{animation:rise .34s cubic-bezier(.2,.7,.3,1) both}
  @keyframes rise{from{opacity:0;transform:translateY(7px)}to{opacity:1;transform:none}}
}
@media print{.rail,.topbar{display:none}.shell{display:block}}
"""

JS = r"""
const D = window.__BRAIN__;
const TICK = '<svg viewBox="0 0 12 12" fill="none" stroke="#fff" stroke-width="2.2" stroke-linecap="round"><path d="M2 6.4 4.6 9 10 3"/></svg>';

/* ---- storage: works on GitHub Pages, degrades to memory in sandboxes ---- */
const mem = {};
const store = {
  get(k, f) { try { const v = localStorage.getItem(k); return v === null ? f : JSON.parse(v); }
              catch (e) { return k in mem ? mem[k] : f; } },
  set(k, v) { try { localStorage.setItem(k, JSON.stringify(v)); } catch (e) { mem[k] = v; } }
};
let done = store.get('brain.nodes', {});
let checks = store.get('brain.checks', {});
let repo = store.get('brain.repo', '');

const esc = s => String(s).replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const el = id => document.getElementById(id);
/* A path that exists links to the file. A path that does not yet exist links to
   GitHub's new-file editor, prefilled with exactly that path — so an unwritten
   concept is one click from an open editor instead of a 404. */
const link = (path, label, exists = true) => {
  const text = esc(label || path);
  if (!repo) return text;
  const base = esc(repo.replace(/\/$/, ''));
  return exists
    ? `<a href="${base}/blob/${D.branch}/${esc(path)}" target="_blank" rel="noopener">${text}</a>`
    : `<a class="tocreate" href="${base}/new/${D.branch}?filename=${encodeURIComponent(path)}" target="_blank" rel="noopener" title="Not written yet — opens a new file at this path">${text}</a>`;
};

/* ---- coverage ---- */
const allNodes = D.chains.flatMap(c => c.nodes);
const doneCount = () => allNodes.filter(n => done[n.id]).length;

function paintCoverage() {
  const cov = el('cov');
  if (!cov) return;
  const pct = Math.round(doneCount() / allNodes.length * 100);
  cov.textContent = pct + '%';
  el('covsub').textContent = doneCount() + ' of ' + allNodes.length + ' concepts written';
  D.chains.forEach(c => {
    const d = c.nodes.filter(n => done[n.id]).length;
    const row = document.querySelector(`[data-chain="${c.n}"]`);
    if (row) {
      row.querySelector('.pct').textContent = d + '/' + c.nodes.length;
      row.querySelectorAll('.dot').forEach((dot, i) => dot.classList.toggle('on', !!done[c.nodes[i].id]));
    }
  });
}

function toggleNode(id) {
  done[id] ? delete done[id] : done[id] = 1;
  store.set('brain.nodes', done);
  document.querySelectorAll(`[data-node="${id}"]`).forEach(n => n.classList.toggle('done', !!done[id]));
  paintCoverage();
}

/* ---- sections ---- */
const SECTIONS = {};

SECTIONS.overview = () => `
  <p class="eyebrow">Control panel · generated ${esc(D.generated)}</p>
  <h2>The permanent brain of an SEO career</h2>
  <p class="lede">Eleven folders, ${allNodes.length} concepts on ${D.chains.length} dependency chains, ${D.templates.length} templates, and a set of rituals that turn every day's work into something reusable. This page is generated from the repository itself — it lives inside it and needs no account, no service and no internet to read.</p>

  <div class="map">
    <div class="map-head">
      <div>
        <h3>Master knowledge map</h3>
        <p>Each row is a chain of real dependencies, not a topic list. Tick a concept when its note exists and is linked. Progress is saved in this browser.</p>
      </div>
      <div class="coverage"><b id="cov">0%</b><span id="covsub">—</span></div>
    </div>
    ${D.chains.map(c => `
      <button class="chain-row" data-chain="${c.n}" data-go="knowledge" data-focus="chain-${c.n}">
        <span class="cn">${String(c.n).padStart(2,'0')}</span>
        <span class="cname">${esc(c.name)}</span>
        <span class="dots">${c.nodes.map(() => '<i class="dot"></i>').join('')}</span>
        <span class="pct">0/${c.nodes.length}</span>
      </button>`).join('')}
  </div>

  <div class="panel">
    <h3>The three rules everything else follows</h3>
    <p class="sub">Break these and the system decays into an unsearchable folder of notes.</p>
    <table><tbody>
      <tr><td style="width:30px"><code>1</code></td><td><b>One canonical location per asset.</b> A checklist exists once. Everything else links to it.</td></tr>
      <tr><td><code>2</code></td><td><b>Every file follows the documentation standard.</b> Frontmatter is not optional, not even on a quick note.</td></tr>
      <tr><td><code>3</code></td><td><b>Every note declares its connections</b> — prerequisites, related, next — on both ends.</td></tr>
    </tbody></table>
    <div class="pills">
      ${D.statuses.map(s => `<span class="pill ${s.status}"><i></i>${esc(s.status)}</span>`).join('')}
    </div>
  </div>

  <div class="panel">
    <h3>Point this page at your repository</h3>
    <p class="sub">Paste your GitHub URL and every file path below becomes a live link to the file itself.</p>
    <div class="repo">
      <input id="repoin" placeholder="https://github.com/you/seo-brain" value="${esc(repo)}" spellcheck="false">
      <button class="act" id="reposave">Save</button>
    </div>
    <p class="note">Stored in this browser only. Nothing is sent anywhere — this page makes no network requests.</p>
  </div>`;

SECTIONS.folders = () => `
  <div class="sec-h"><p class="eyebrow">Structure</p><h2>Eleven folders</h2>
  <p class="lede">Numbered so the order is deliberate, with gaps so a new domain can be inserted in ten years without renaming anything. Renaming breaks links; gaps prevent renaming.</p></div>
  <div class="grid g2">
    ${D.folders.map(f => `
      <div class="fcard">
        <span class="fp">${link(f.path + '/README.md', f.path + '/', f.exists)}</span>
        <h4>${esc(f.tagline)}</h4>
        <p>${esc(f.purpose)}</p>
        <div class="n">${f.files} file${f.files === 1 ? '' : 's'} committed</div>
      </div>`).join('')}
  </div>`;

SECTIONS.knowledge = () => `
  <div class="sec-h"><p class="eyebrow">Curriculum</p><h2>Knowledge chains</h2>
  <p class="lede">Work left to right. Every arrow is a dependency: a concept you cannot properly understand until the one before it is solid. Tick a node when the note exists, is linked in both directions, and you could teach it.</p>
  <p class="note" style="max-width:64ch">Solid paths link to a committed file. <span style="border-bottom:1px dashed var(--rule);color:var(--ink-3)">Dashed paths</span> are notes that do not exist yet — clicking one opens a new file on GitHub at exactly that path, ready for the concept template.</p></div>
  ${D.chains.map(c => `
    <div class="chain-card" id="chain-${c.n}">
      <header>
        <h3>${String(c.n).padStart(2,'0')} · ${esc(c.name)}</h3>
        <span class="home">${esc(c.home)}/</span>
      </header>
      <ul class="ladder">
        ${c.nodes.map(n => `
          <li class="node ${done[n.id] ? 'done' : ''}" data-node="${esc(n.id)}">
            <button class="tick" data-tick="${esc(n.id)}" aria-label="Mark ${esc(n.title)} as written">${TICK}</button>
            <span class="body">
              <span class="t">${esc(n.title)}</span><br>
              <span class="p">${link(n.path, null, n.exists)}</span>
            </span>
          </li>`).join('')}
      </ul>
    </div>`).join('')}
  <div class="panel">
    <h3>Cross-cutting bridges</h3>
    <p class="sub">Chains intersect. These links carry the most value in the repository, and each is declared in both notes.</p>
    <table><tbody>${D.bridges.map(b => `<tr><td><b>${esc(b.pair)}</b></td><td>${esc(b.why)}</td></tr>`).join('')}</tbody></table>
  </div>`;

SECTIONS.playbooks = () => `
  <div class="sec-h"><p class="eyebrow">15-business-playbooks</p><h2>Industry playbooks</h2>
  <p class="lede">A playbook is not general SEO applied to a vertical. It is the set of decisions that are <em>different</em> for that vertical. If a section could be copied into another playbook unchanged, it belongs in the encyclopedia instead.</p></div>
  <div class="grid g2">
    ${D.playbooks.map(p => `
      <div class="fcard">
        <span class="fp">${link('15-business-playbooks/' + p.slug + '.md', p.slug + '.md', p.exists)}</span>
        <h4>${esc(p.name)}</h4>
        <p>${esc(p.note)}</p>
      </div>`).join('')}
  </div>
  <div class="panel">
    <h3>What every playbook contains</h3>
    <p class="sub">Twelve fixed sections, so two playbooks can be compared side by side.</p>
    <table><tbody>
      ${D.playbookSections.map((s, i) => `<tr><td style="width:34px"><code>${String(i+1).padStart(2,'0')}</code></td><td>${esc(s)}</td></tr>`).join('')}
    </tbody></table>
    <p class="note"><b>Evidence log.</b> Each playbook ends with what you have actually observed, with dates and clients. A playbook with a filled evidence log is a sellable asset. Without one it is a blog post.</p>
  </div>`;

SECTIONS.operations = () => `
  <div class="sec-h"><p class="eyebrow">20-operations</p><h2>Operations</h2>
  <p class="lede">The difference between knowing SEO and shipping it repeatably, for the fortieth time, in three hours.</p></div>
  <div class="panel">
    <h3>Client deliverables library</h3>
    <p class="sub">Every document a client ever receives has a template. Nothing is built from scratch again.</p>
    <div class="grid g3">${D.deliverables.map(d => `<div class="pill">${esc(d)}</div>`).join('')}</div>
    <p class="note">Each template carries an internal instruction block inside HTML comments, so it disappears from the client-facing render, and a version stamp recorded on the sent document.</p>
  </div>
  <div class="panel">
    <h3>Agency simulator</h3>
    <p class="sub">When there is no live client, the practice supplies the work — judged by the same checklists as paid work.</p>
    <table><tbody>${D.simulations.map(s => `<tr><td style="width:38%"><b>${esc(s.name)}</b></td><td>${esc(s.note)}</td></tr>`).join('')}</tbody></table>
    <p class="note">Every simulation must leave a trace in the repository. One that does not was entertainment, not practice.</p>
  </div>
  <div class="panel">
    <h3>Client engagement lifecycle</h3>
    <p class="sub">Each stage consumes a template and produces a filed artifact.</p>
    <pre>Lead
 └─ Proposal ─────────── 30-clients/&lt;client&gt;/01-proposal/
     └─ Discovery ────── 02-discovery/
         └─ Audit ────── 03-audits/
             └─ Strategy ── 04-strategy/
                 └─ Delivery loop ── 05-deliverables/ + 06-reporting/
                     └─ Close
                         ├─ Portfolio graduation → 40-portfolio/
                         ├─ SOP improvements → 20-operations/
                         ├─ Lessons + mistakes → 60-journal/
                         └─ Archive → 90-archive/</pre>
  </div>`;

SECTIONS.content = () => `
  <div class="sec-h"><p class="eyebrow">50-content-engine</p><h2>Content engine</h2>
  <p class="lede">One concept, eleven assets, all derived from the same source note. Write an asset from memory and your eleven outputs will quietly contradict each other within a year.</p></div>
  <div class="panel">
    <table><thead><tr><th>#</th><th>Asset</th><th>Its one job</th></tr></thead><tbody>
      ${D.formats.map((f, i) => `<tr><td><code>${String(i+1).padStart(2,'0')}</code></td><td><b>${esc(f.name)}</b></td><td>${esc(f.job)}</td></tr>`).join('')}
    </tbody></table>
  </div>
  <div class="panel">
    <h3>Staleness</h3>
    <p class="sub">Each asset set tracks per-format status: not started, drafted, published, or needs update.</p>
    <p style="margin:0;font-size:13.5px">When a source concept changes materially, every asset in its set is flagged <code>needs update</code> rather than left to rot. This is the mechanism that keeps a two-year-old YouTube video from teaching something you stopped believing eighteen months ago.</p>
  </div>`;

SECTIONS.rituals = () => `
  <div class="sec-h"><p class="eyebrow">Workflows</p><h2>Rituals</h2>
  <p class="lede">A repository without rituals becomes a graveyard. Progress here is saved in this browser; reset it at the start of each cycle.</p></div>
  <div class="panel">
    <h3>The harvest loop · daily, 15 minutes</h3>
    <p class="sub">Everything learned becomes repository assets the same day. Nothing waits for "when I have time to write it up".</p>
    <table><tbody>${D.harvest.map(h => `<tr><td style="width:26%"><b>${esc(h.stage)}</b></td><td><code>${esc(h.path)}</code><br><span style="color:var(--ink-3)">${esc(h.note)}</span></td></tr>`).join('')}</tbody></table>
    <p class="note">Definition of done for a learning day: the journal entry lists every file created or updated, by path. Empty list, nothing permanent.</p>
  </div>
  <div class="panel">
    <div class="copybar"><div><h3>Weekly review</h3><p class="sub" style="margin:0">Sunday, 45 minutes</p></div>
      <button class="act" data-reset="w">Reset</button></div>
    <ul class="chk">${D.weekly.map((t, i) => `
      <li class="${checks['w'+i] ? 'done' : ''}"><input type="checkbox" id="w${i}" data-chk="w${i}" ${checks['w'+i] ? 'checked' : ''}><label for="w${i}">${esc(t)}</label></li>`).join('')}
    </ul>
  </div>
  <div class="panel">
    <div class="copybar"><div><h3>Monthly review</h3><p class="sub" style="margin:0">Last day of the month, 90 minutes</p></div>
      <button class="act" data-reset="m">Reset</button></div>
    <ul class="chk">${D.monthly.map((t, i) => `
      <li class="${checks['m'+i] ? 'done' : ''}"><input type="checkbox" id="m${i}" data-chk="m${i}" ${checks['m'+i] ? 'checked' : ''}><label for="m${i}">${esc(t)}</label></li>`).join('')}
    </ul>
  </div>`;

SECTIONS.standard = () => `
  <div class="sec-h"><p class="eyebrow">00-meta</p><h2>Documentation standard</h2>
  <p class="lede">Second brains do not fail from lack of content. They fail from inconsistency — three formats for one note type, four names for one tag, links pointing nowhere.</p></div>
  <div class="panel">
    <h3>Frontmatter</h3>
    <p class="sub">Opens every file in the repository.</p>
    <table><thead><tr><th>Field</th><th>Value</th><th>Rule</th></tr></thead><tbody>
      ${D.frontmatter.map(f => `<tr><td><code>${esc(f.field)}</code></td><td>${esc(f.value)}</td><td style="color:var(--ink-3)">${esc(f.note)}</td></tr>`).join('')}
    </tbody></table>
  </div>
  <div class="panel">
    <h3>Status lifecycle</h3>
    <table><thead><tr><th>Status</th><th>Meaning</th><th>Bar to clear</th></tr></thead><tbody>
      ${D.statuses.map(s => `<tr><td><span class="pill ${s.status}"><i></i>${esc(s.status)}</span></td><td>${esc(s.meaning)}</td><td style="color:var(--ink-3)">${esc(s.bar)}</td></tr>`).join('')}
    </tbody></table>
  </div>
  <div class="panel">
    <h3>Non-negotiables</h3>
    <table><tbody>${D.rules.map((r, i) => `<tr><td style="width:34px"><code>${String(i+1).padStart(2,'0')}</code></td><td>${esc(r)}</td></tr>`).join('')}</tbody></table>
  </div>
  <div class="panel">
    <h3>Concept body</h3>
    <p class="sub">Fixed section order, so any note can be read at speed.</p>
    <pre>Definition (one sentence, client-safe)
Why it matters (business impact)
How it works (mechanics)
How I apply it (my method — what makes this note mine)
Common mistakes (linked to the mistake journal)
Connections (prerequisites / related / next / used in)
Open questions (the most valuable section in a seed note)
Sources
Changelog</pre>
  </div>`;

SECTIONS.templates = () => `
  <div class="sec-h"><p class="eyebrow">00-meta/templates</p><h2>Template library</h2>
  <p class="lede">No file in this repository is created from scratch. Open one, copy it, fill it in, delete the instruction comments.</p></div>
  <div class="tlist">
    ${D.templates.map((t, i) => `
      <details class="titem">
        <summary>
          <span><span class="tt">${esc(t.title)}</span><span class="tm">${esc(t.file)} · ${esc(t.type)} · v${esc(t.version)} · ${t.lines} lines</span></span>
          <span class="act">Open</span>
        </summary>
        <div class="tbody">
          <div class="copybar">
            <span class="tm">${link(t.path)}</span>
            <button class="act" data-copy="tpl-${i}">Copy template</button>
          </div>
          <pre id="tpl-${i}">${esc(t.body)}</pre>
        </div>
      </details>`).join('')}
  </div>`;

SECTIONS.briefing = () => `
  <div class="sec-h"><p class="eyebrow">Portability</p><h2>Agent briefing</h2>
  <p class="lede">This repository must never depend on one AI account, one chat history or one vendor. Paste this block into any assistant, anywhere, and it will understand the system in one message.</p></div>
  <div class="panel">
    <div class="copybar">
      <span class="tm">${link('00-meta/AGENT-BRIEFING.md')}</span>
      <button class="act" data-copy="brief">Copy briefing</button>
    </div>
    <pre id="brief">${esc(D.briefing)}</pre>
  </div>
  <div class="panel">
    <h3>Rebuilding this page</h3>
    <p class="sub">The page is generated from the repository, so it never drifts out of date.</p>
    <pre>python3 tools/build-dashboard.py</pre>
    <p class="note">No dependencies beyond Python 3.8. Commit the regenerated <code>index.html</code> and GitHub Pages updates within a minute.</p>
  </div>`;

/* ---- search ---- */
const INDEX = [
  ...D.folders.map(f => ({ t: f.path + ' — ' + f.tagline, k: 'folder', go: 'folders' })),
  ...D.chains.map(c => ({ t: c.name, k: 'chain', go: 'knowledge', focus: 'chain-' + c.n })),
  ...D.chains.flatMap(c => c.nodes.map(n =>
      ({ t: n.title, k: 'concept · ' + c.name, go: 'knowledge', focus: 'chain-' + c.n }))),
  ...D.templates.map(t => ({ t: t.title, k: 'template', go: 'templates' })),
  ...D.playbooks.map(p => ({ t: p.name + ' playbook', k: 'playbook', go: 'playbooks' })),
  ...D.deliverables.map(d => ({ t: d, k: 'deliverable', go: 'operations' })),
  ...D.simulations.map(s => ({ t: s.name, k: 'simulation', go: 'operations' })),
  ...D.formats.map(f => ({ t: f.name, k: 'content asset', go: 'content' })),
  ...D.frontmatter.map(f => ({ t: f.field + ' — ' + f.value, k: 'standard', go: 'standard' })),
  ...D.weekly.map(w => ({ t: w, k: 'weekly review', go: 'rituals' })),
  ...D.monthly.map(m => ({ t: m, k: 'monthly review', go: 'rituals' })),
];

function runSearch(q) {
  const box = el('view');
  const hits = INDEX.filter(r => r.t.toLowerCase().includes(q.toLowerCase())).slice(0, 60);
  box.innerHTML = `
    <div class="sec-h"><p class="eyebrow">Search</p><h2>${hits.length} match${hits.length === 1 ? '' : 'es'} for "${esc(q)}"</h2></div>
    ${hits.length ? `<div class="results">${hits.map(h => `
      <button class="result" data-go="${h.go}" ${h.focus ? `data-focus="${h.focus}"` : ''}>
        <span class="rt">${esc(h.t)}</span><span class="rk">${esc(h.k)}</span>
      </button>`).join('')}</div>`
    : `<div class="empty">Nothing matches. Try a concept, a template name or an industry.</div>`}`;
  document.querySelectorAll('.nav button').forEach(b => b.setAttribute('aria-current', 'false'));
}

/* ---- routing ---- */
function show(name, focus) {
  const s = SECTIONS[name] || SECTIONS.overview;
  el('view').innerHTML = s();
  document.querySelectorAll('.nav button').forEach(b =>
    b.setAttribute('aria-current', String(b.dataset.go === name)));
  if (name === 'overview') paintCoverage();
  if (focus) {
    const target = el(focus);
    if (target) target.scrollIntoView({ behavior: 'smooth', block: 'start' });
  } else {
    window.scrollTo({ top: 0 });
  }
  try { if (location.hash.slice(1) !== name) history.replaceState(null, '', '#' + name); }
  catch (e) { /* file:// or sandboxed — navigation still works via the rail */ }
}

/* ---- events ---- */
document.addEventListener('click', e => {
  const go = e.target.closest('[data-go]');
  if (go) { show(go.dataset.go, go.dataset.focus); return; }

  const tick = e.target.closest('[data-tick]');
  if (tick) { toggleNode(tick.dataset.tick); return; }

  const copy = e.target.closest('[data-copy]');
  if (copy) {
    const text = el(copy.dataset.copy).textContent;
    const done = () => { const o = copy.textContent; copy.textContent = 'Copied'; copy.classList.add('on');
      setTimeout(() => { copy.textContent = o; copy.classList.remove('on'); }, 1400); };
    if (navigator.clipboard) { navigator.clipboard.writeText(text).then(done, fallback); } else { fallback(); }
    function fallback() {
      const ta = document.createElement('textarea');
      ta.value = text; ta.style.position = 'fixed'; ta.style.opacity = '0';
      document.body.appendChild(ta); ta.select();
      try { document.execCommand('copy'); done(); } catch (err) { copy.textContent = 'Select and copy'; }
      ta.remove();
    }
    return;
  }

  const reset = e.target.closest('[data-reset]');
  if (reset) {
    const p = reset.dataset.reset;
    Object.keys(checks).forEach(k => { if (k[0] === p) delete checks[k]; });
    store.set('brain.checks', checks);
    show('rituals');
    return;
  }

  if (e.target.id === 'reposave') {
    repo = el('repoin').value.trim().replace(/\/$/, '');
    store.set('brain.repo', repo);
    show('overview');
  }
});

document.addEventListener('change', e => {
  const c = e.target.closest('[data-chk]');
  if (!c) return;
  const k = c.dataset.chk;
  c.checked ? checks[k] = 1 : delete checks[k];
  store.set('brain.checks', checks);
  c.closest('li').classList.toggle('done', c.checked);
});

const searchbox = el('q');
searchbox.addEventListener('input', () => {
  const q = searchbox.value.trim();
  q.length > 1 ? runSearch(q) : show(location.hash.slice(1) || 'overview');
});
document.addEventListener('keydown', e => {
  if (e.key === '/' && document.activeElement !== searchbox) { e.preventDefault(); searchbox.focus(); }
  if (e.key === 'Escape' && document.activeElement === searchbox) { searchbox.value = ''; searchbox.blur(); show('overview'); }
});

window.addEventListener('hashchange', () => show(location.hash.slice(1) || 'overview'));
show(location.hash.slice(1) || 'overview');
"""

HTML = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>SEO Brain — control panel</title>
<meta name="description" content="The permanent knowledge system for an SEO career: knowledge chains, playbooks, operations, templates and rituals.">
<meta name="color-scheme" content="light">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@500;600;700&family=IBM+Plex+Sans:wght@400;500;600&family=IBM+Plex+Mono:wght@400;500&display=swap" rel="stylesheet">
<style>__CSS__</style>
</head>
<body>
<div class="shell">
  <aside class="rail">
    <div class="brand">
      <h1>SEO Brain</h1>
      <p>Second brain · v0.2</p>
    </div>
    <nav class="nav">
      <button data-go="overview"><span class="num">00</span>Overview</button>
      <button data-go="folders"><span class="num">01</span>Structure</button>
      <button data-go="knowledge"><span class="num">02</span>Knowledge chains</button>
      <button data-go="playbooks"><span class="num">03</span>Playbooks</button>
      <button data-go="operations"><span class="num">04</span>Operations</button>
      <button data-go="content"><span class="num">05</span>Content engine</button>
      <button data-go="rituals"><span class="num">06</span>Rituals</button>
      <button data-go="standard"><span class="num">07</span>Standard</button>
      <button data-go="templates"><span class="num">08</span>Templates</button>
      <button data-go="briefing"><span class="num">09</span>Agent briefing</button>
    </nav>
    <div class="rail-foot">
      Generated from the repository by<br><code>tools/build-dashboard.py</code>
    </div>
  </aside>
  <main>
    <div class="topbar">
      <div class="search">
        <input id="q" type="search" placeholder="Search concepts, templates, playbooks" spellcheck="false" aria-label="Search">
        <span class="hint">/</span>
      </div>
    </div>
    <div class="wrap" id="view"></div>
  </main>
</div>
<script>window.__BRAIN__ = __DATA__;</script>
<script>__JS__</script>
</body>
</html>
"""


def main():
    payload = build_payload()
    if not payload["templates"]:
        print("warning: no templates found — run from the repository root", file=sys.stderr)
    html = (HTML
            .replace("__CSS__", CSS)
            .replace("__DATA__", json.dumps(payload, ensure_ascii=False).replace("</", "<\\/"))
            .replace("__JS__", JS))
    out = os.path.join(ROOT, "index.html")
    with open(out, "w", encoding="utf-8") as fh:
        fh.write(html)
    kb = os.path.getsize(out) / 1024
    print("wrote %s (%.0f KB)" % (out, kb))
    print("  %d folders · %d chains · %d concepts · %d templates" % (
        len(payload["folders"]), len(payload["chains"]),
        sum(len(c["nodes"]) for c in payload["chains"]), len(payload["templates"])))


if __name__ == "__main__":
    main()
