---
name: world-intel-daily
description: Daily world intelligence sweep. Reads RSS, fills topic gaps with web search, and appends a dated analyst digest to 00_Inbox/WORLD-INTEL-LIVE.md. Invoke with /world-intel-daily.
---

# World Intel: Daily Sweep

You are running an analyst sweep, not writing a news feed. Work through the six
steps in order. This skill often runs unattended on a schedule: never ask the
user a question, never wait for approval, and always finish with the Output step.

## Step 1: Date verification

1. Confirm today's actual date with one web search. System dates can drift. Also
   run `date`. If they disagree, trust the web result.
2. Read 00_Inbox/WORLD-INTEL-LIVE.md and find the `Last Digest:` timestamp.
   If the file does not exist, create it from
   02_Areas/World-Intelligence/_Templates/live-file-template.md.
3. Coverage window N = days between Last Digest and today. Minimum 1, maximum 7.
   If Last Digest is empty, N = 1.
4. If a digest dated today already exists in the live file, do not write a second
   one. Go straight to the Output step using the existing digest.

## Step 2: RSS ingest (two passes)

Pass 1. Run: python3 .claude/scripts/rss_ingest.py --days N
Output is a flat list: source | date | title | short description | link

Pass 2. Mark every item RELEVANT or SKIP using the topic areas in Step 4 and the
noise filter in Step 5. Only RELEVANT items move forward.

Source-specific rules:
- Hacker News: titles only (descriptions are just comment links). Skip anything
  where you cannot tell from the title alone what it is about.
- myFT: use both title and summary. FT summaries carry useful topic context.
- All others: title and description together.

Volume control:
- SCMP: max 4 items. Al Jazeera: max 4 items.
- Bloomberg: max 6 items. WSJ (World + Economy combined): max 6 items.
- Creator Economy & Marketing (ICYMI by Lia Haberman, Tubefilter, Digiday,
  Link in Bio by Rachel Karten): max 3 items each.
- Tier 1 sources (MIT Technology Review, Every): uncapped. Include everything
  relevant.
- Solo writers (Stoller, Noah Smith, Karpathy, Rubinstein, Azhar, Chamath,
  Paul Graham, Interconnects, Fabricated Knowledge): their signal density is
  higher, so lean toward including their posts.

## Step 3: Deep-dive on top items

Pick the 5 to 8 most significant items. For each, go deeper using this strict
priority order, stopping as soon as you have enough. This protects token budget.
1. The RSS content itself (often enough)
2. Full article fetch via WebFetch, if the item has a link
3. Your own knowledge, for well-known topics
4. Perplexity search, only when the above are not enough

## Step 4: Gap-fill via web search

After RSS, list the topic areas with zero RSS coverage. For those gaps only, run
targeted Perplexity searches (perplexity_search).

Topic tiers:
- Tier 1 (always check): Geopolitics, US Macro, Global Macro, US-China, AI,
  Business/Finance, Tech, Social Media, Digital Marketing
- Tier 2 (check only if the coverage gap N is 2 days or more): EU, Accounting/Tax, Startups/VC, Privacy/Crypto, Climate/Energy,
  Central bank policy, AI ethics/regulation, US housing/credit,
  Fiscal policy/debt, India-pakistan, India-china
- Tier 3 (only if something exceptional happened): Neurotechnology,
  Fusion/Space, Natural World, Culture, NYC Local

## Step 5: Noise filter

Hard skips, always:
- Pop culture, celebrity, sports
- Day-to-day price movements (stocks, crypto, forex)
- Political drama with no structural significance
- Isolated one-off events with no trend connection
- Press releases and corporate PR
- Stories that will be forgotten in two weeks
- Creator and marketing tips, how-tos, listicles and tactical advice. From
  creator and marketing sources, keep only structural news: platform algorithm
  or monetization changes, marketing budget shifts, regulation, and major deals.

## Step 6: Write the digest

Append a new dated section to 00_Inbox/WORLD-INTEL-LIVE.md, following the layout
in 02_Areas/World-Intelligence/_Templates/live-file-template.md exactly.

Each surviving item gets:
- A headline with source and URL
- A Signal annotation: 1 to 2 sentences on significance and second-order effects
- A Read line with source URLs

Grouping:
- Group related items under their topic area heading.
- When two items from different topic areas connect, place them adjacent and add
  a line starting: ↳ Together these suggest:

Manual items: if the live file contains items tagged [MANUAL] with no Signal
line, annotate them now in the same format.

Close the digest with a Predictions section: 3 bold, speculative claims based on
the week's signal so far. They are meant to sharpen thinking, not assert
certainty. Before writing them, scan 07_Context/World-Intelligence/ and reference
any existing trend note a prediction builds on or contradicts.

End with the footer line: [X] items across [Y] topics, covering [date range].
If N > 1, the section heading says: covering N days.

Finally, update the `Last Digest:` line at the top of the live file to today.

## Analyst posture (applies to every item)

- Every item gets a "so what". No bare headlines.
- Distinguish signal (one data point) from trend (a pattern across time).
- Note when something is quiet but important: the structural shift that barely
  made headlines.
- Triangulate on political stories. Actively seek multiple perspectives and note
  when a narrative is being spun.
- Follow the money: who profits, who loses, what does capital flow tell us?
- Apply these meta-lenses across all topics: emergence and spontaneous order;
  quiet leverage (small signals compounding); revolutionary ideas gaining
  traction; prediction market movements.

## Output (always do this last)

Write today's digest section, and only today's, to .claude/logs/last-daily.md,
overwriting the file. Put a 3-line "If you read nothing else" summary at the
very top. This file is what gets emailed. If any step failed (script error,
Perplexity unavailable), still write the file and state plainly at the top what
failed and what was skipped.
