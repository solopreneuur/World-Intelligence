---
created: 2026-03-20
para: inbox
tags: [documentation, world-intel, guide]
---

# World Intelligence System — How It Works

This is a full breakdown of the automated world intelligence layer I've built into my second brain. If you want to rebuild this yourself, everything you need is here.

---

## The Problem It Solves

Reading the news is noisy, time-consuming, and often useless. Most news is either irrelevant to what you care about, driven by narrative rather than facts, or too surface-level to be actionable. I wanted something different: a system that acts like a smart analyst sweep — every day, while I'm not looking, it reads across sources I've curated, filters for signal over noise, and leaves me a digest with actual "so what" thinking baked in.

The output isn't a news feed. It's a running intelligence file, structured by topic, with second-order analysis on every item. At the end of the week, the best material gets compressed into durable trend notes that build up over time into a model of how the world is changing.

---

## The Architecture

Three moving parts: 
1. **Daily Sweep** (`/world-intel-daily`) — reads RSS, fills gaps via web search, appends a dated digest to a live file
2. **Weekly Compression** (`/world-intel-weekly`) — synthesizes the week's live file into a structured briefing, promotes durable trends to a permanent Context layer, resets the live file
3. **Trend Notes** (`/trend-note`) — standalone deep-research tool; lets you go deep on any topic and create a permanent, sourced note in the knowledge base

These run as Claude Code skills (Claude Code is Anthropic's CLI tool). You invoke them as slash commands in a terminal session pointed at your vault directory. Claude handles everything: reading the RSS data, running web searches via Perplexity, writing to files.

---

## The RSS Feed — Sources & Curation Philosophy

The RSS plugin (Obsidian RSS Dashboard) stores all feed data in a local JSON file. The daily skill reads this file directly via a Python script, extracts headlines from the last N days, and filters for relevance. No external RSS reader needed at runtime.

### The 22 sources I subscribe to

**Wire / General News**
- Al Jazeera — international perspective, especially non-Western angles
- South China Morning Post — China and Asia-Pacific, incl. HK
- WSJ World News + WSJ Economy
- myFT (Financial Times custom feed — follows topics I've selected)
- Bloomberg Economics

**Tech & AI**
- MIT Technology Review — deep tech analysis, not hype
- Hacker News — signal from the dev community (headlines only; no comments)
- TechCrunch — startup and product news
- The Information — paywalled premium tech reporting
- Interconnects AI — ML/AI research-level analysis
- Fabricated Knowledge — semiconductor industry deep dives
- Andrej Karpathy's blog — rare, high-signal posts from one of the best AI researchers

**Finance & Economics**
- Net Interest (Marc Rubinstein) — banking and financial markets analysis
- Exponential View (Azeem Azhar) — tech + economy intersections
- BIG by Matt Stoller — antitrust, corporate power, monopoly dynamics
- Bloomberg Economics (also under tech — central bank, macro)

**Independent / High-Signal Writers**
- Every — essays on tech, business, AI; very high quality per piece
- Noahpinion (Noah Smith) — macro economics, politics, tech with strong takes
- Chamath Palihapitiya — VC perspective, macro views, contrarian angles
- Paul Graham Essays — rare, worth catching when he publishes
- Palladium Magazine — long-form on governance, history, political economy

**Startups / VC**
- Venture Daily Digest — curated VC and startup deal flow

### Curation philosophy: designed for balance

I deliberately built in diversity across several axes:

**Political/economic angle:** WSJ and Bloomberg sit next to Matt Stoller (who is anti-corporate power) and Noah Smith (centrist economist). Chamath represents tech VC optimism; Palladium challenges mainstream governance assumptions. No single worldview dominates.

**Geographic lens:** Al Jazeera + SCMP give non-Western framing on global events. FT gives European/global finance perspective. This prevents the default US-centric filter.

**Signal depth:** Wire services (Al Jazeera, SCMP, WSJ) give breadth. Solo writers (Stoller, Smith, Karpathy, Rubinstein) give depth and original analysis you won't find replicated elsewhere. The mix means you catch both breaking developments and slow structural trends.

**Sector coverage:** The feed covers AI/tech, geopolitics, macro/finance, antitrust/power, and VC — the five areas I actually care about. I don't subscribe to sources outside those domains, which keeps the filter tight.

**Volume control:** High-volume wire sources are capped (4 items from SCMP or Al Jazeera; 6 from Bloomberg/WSJ). Tier 1 sources (MIT Tech Review, Every) are uncapped — include everything relevant. Solo writers get a higher-than-default inclusion threshold because their signal density is higher.

---

## The Daily Sweep — Step by Step

When you run `/world-intel-daily`, here's what happens:

### 1. Date verification
Claude checks today's actual date via web search (system dates can drift). It then reads the live file to find the `Last Digest:` timestamp and calculates how many days to cover.

### 2. RSS ingest (two-pass)
A Python script reads the Obsidian RSS plugin's JSON data file and extracts all items published in the coverage window. Output: flat list of `[source] | [date] | [title] | [short description]`.

Pass 1 produces the raw list. Pass 2 filters it: each item gets marked ✅ RELEVANT or ❌ SKIP based on topic areas and the noise filter. Only ✅ items move forward.

**Source-specific rules baked in:**
- Hacker News: titles only (descriptions are just comment links). Skip anything where you can't tell from the title alone what it's about.
- myFT: use both title and summary — FT's summaries contain useful topic context.
- All others: title + description together.

### 3. Deep-dive on top items
For the 5–8 most significant items, Claude goes deeper using a strict priority order to avoid blowing token budget:
1. RSS content itself (often enough)
2. Full article fetch via WebFetch (if the RSS item has a link)
3. Model's own knowledge (for well-known topics)
4. Perplexity search (only when the above aren't enough)

### 4. Gap-fill via web search
After processing RSS, Claude identifies topic areas with zero RSS coverage. For those gaps, it runs targeted Perplexity searches. Topic tiers determine what always gets checked vs. what only gets checked on multi-day gaps.

**Topic tiers:**
- Tier 1 (always): Geopolitics, US Macro, Global Macro, US-China, AI, Business/Finance, Tech
- Tier 2 (check if gap ≥ 2 days): EU/Germany, Migration, Accounting/Tax, Startups/VC, Privacy/Crypto, Climate/Energy, Central bank policy, AI ethics/regulation, US housing/credit, Fiscal policy/debt
- Tier 3 (only if exceptional): Neurotechnology, Fusion/Space, Natural World, Culture, NYC Local

### 5. Noise filter
Hard skips, always:
- Pop culture, celebrity, sports
- Day-to-day price movements (stocks, crypto, forex)
- Political drama with no structural significance
- Isolated one-off events with no trend connection
- Press releases and corporate PR
- Stories that will be forgotten in two weeks

### 6. Writing the digest
Each surviving item gets:
- A headline with source and URL
- A *Signal:* annotation (1–2 sentences on significance and second-order effects)
- A *Read:* line with source URLs

Related items from the same topic area get grouped, and when two items from different topic areas connect, they get placed adjacent with a `↳ Together these suggest:` note.

The digest closes with a **Predictions** section: 3 bold, speculative claims based on the week's signal, intended to sharpen thinking rather than assert certainty.

### The analyst posture
The system is explicitly designed to think like an analyst, not a journalist:
- Every item gets a "so what." No bare headlines.
- Distinguish signal (one data point) from trend (pattern across time).
- Note when something is *quiet but important* — the structural shift that barely made headlines.
- Triangulate on political stories — actively seek multiple perspectives, note when a narrative is being spun.
- Follow the money: who profits, who loses, what does capital flow tell us?
- Apply meta-lenses across all topics: emergence & spontaneous order, quiet leverage (small signals compounding), revolutionary ideas gaining traction, prediction market movements.

---

## The Weekly Compression — Step by Step

Run on Sundays (or whenever). Takes the accumulated week of daily digests and turns them into something durable.

### 1. Read everything
Full read of the live file + a scan of existing trend notes in Context to check for continuations or contradictions.

### 2. Synthesize
Works through the week looking for:
- **Top 5–7 Signals** — ranked by structural significance, not media volume
- **Emerging Patterns** — two or more signals pointing the same direction; named as a phrase, not a paragraph
- **Quiet But Important** — slow-moving structural things that barely made noise
- **Cross-Topic Connections** — intersections between different topic areas (where original insight lives)
- **Vault Knowledge Activated** — where something this week connects to a book, concept, or framework already in Context
- **Questions to Track** — crisp, specific, unresolved questions worth watching

### 3. Weekly briefing
Creates a dated markdown file in `02_Areas/World-Intelligence/_Briefings/`. Structured document with all synthesis sections, sources linked throughout.

### 4. Compress durable trends to Context
Patterns that have staying power — appearing across 2+ weeks — get promoted to permanent trend notes in `07_Context/World-Intelligence/`. One-week stories stay in the briefing. **This step always requires my explicit approval before writing.**

### 5. Reset the live file
Clears WORLD-INTEL-LIVE.md back to a clean template, ready for next week.

---

## Trend Notes — Deep Research on Demand

The `/trend-note` skill is the standalone research engine. You give it a topic; it does deep research and produces a permanent, structured note.

Use cases:
- You spotted something in a daily sweep and want to go deeper
- A topic has recurred across multiple sweeps and deserves a dedicated note
- You want to proactively research an emerging trend before it shows up in your feed

**How it works:**
1. Checks what's already in the vault on this topic (daily digests, existing trend notes, weekly briefings)
2. Runs a Phase A deep research query via Perplexity (`perplexity_research`) — comprehensive analysis with citations
3. Runs 1–2 Phase B follow-ups via Perplexity (`perplexity_search`) — verify facts, find contrarian POV, pull a recent data point
4. Synthesizes: core claim, evidence (3–6 data points with dates + URLs), significance, counterarguments, open questions, vault connections
5. Shows me a summary before writing anything, gets my sign-off

**Output structure:**

```
07_Context/World-Intelligence/[Trend Name].md

## What This Is
One sharp sentence. Not "AI is changing things" — "Foundation model providers are
vertically integrating into application layers, threatening the independent software
ecosystem built on top of them."

## Evidence
- [Date]: [signal] — *[Source](URL)*

## Significance
Why this matters beyond the surface. Second-order effects. What does it compound into
in 12–36 months?

## Counterarguments & Uncertainty
What would falsify this? What's being missed?

## Open Questions
Specific, testable questions worth watching.

## Related
Wikilinks to vault notes, books, concepts that connect.
```

---

## The Live File — WORLD-INTEL-LIVE.md

This is the staging area. It lives in `00_Inbox/` and accumulates throughout the week. Structure:

```
Last Digest: YYYY-MM-DD     ← timestamp updated by daily skill

## [Date] — Daily Sweep [covering X days if gap > 1]

### [Topic Area]

**[Headline]** — *[Source](URL)*
*Signal:* [significance + second-order effects]
*Read:* [Source](URL)

---

### 🔭 Predictions
1. **[Bold claim]** — [reasoning]
...

---
*[X] items across [Y] topics — covering [date range]*
```

I can also manually drop items into this file with a `[MANUAL]` tag. The daily skill will annotate them automatically on next run.

---

## The Context Layer — 07_Context/World-Intelligence/

This is where durable knowledge lives. Each trend note is a markdown file with rich frontmatter (status, topics, importance, semantic context for search) and the structured sections above. Over time, this builds into a model of how the world is changing — cross-referenced with books, concepts, and frameworks in the broader Context layer.

The system is designed to compound: as more trend notes accumulate, the daily sweep can reference them in its Predictions section, and the weekly compression can explicitly flag when new evidence confirms or contradicts an existing trend.

---

## Tech Stack

| Component | Tool |
|---|---|
| Vault | Obsidian |
| AI runtime | Claude Code (CLI) |
| Web intelligence | Perplexity MCP (via `perplexity_research`, `perplexity_search`) |
| RSS | Obsidian RSS Dashboard plugin (reads local JSON) |
| Skills/commands | `.claude/skills/` directory in vault |
| Knowledge layer | Markdown files + YAML frontmatter in `07_Context/` |

---

## If You're Rebuilding This

**Minimum viable version:**
1. Install Claude Code and point it at your vault
2. Set up an RSS plugin that stores data as JSON (Obsidian RSS Dashboard does this)
3. Configure Perplexity as an MCP server (gives Claude web search capability)
4. Write the daily skill with: RSS parse script → relevance filter → gap search → append to live file
5. Write the weekly skill with: synthesize → create briefing → reset live file

**What matters most:**
- The source list. Be deliberate. Mix wire services with independent writers. Build in geographic diversity. Cap high-volume sources.
- The noise filter. If you don't hard-skip pop culture and price movements, the digest drowns in noise.
- The analyst posture. Every item needs a "so what." Without it, you've just built an RSS reader.
- The prediction section. It forces synthesis and makes the whole thing more useful as a thinking tool.

**What's optional but valuable:**
- The trend note system (adds compounding value over time)
- The vault connection layer (requires a broader knowledge base to connect to)
- The weekly compression (overkill if you're just starting)

Start with the daily sweep. Get the source list right. Add the rest incrementally.
