---
name: trend-note
description: Deep research on one topic, producing a permanent, sourced trend note in 07_Context/World-Intelligence/. Invoke with /trend-note followed by the topic. Interactive only.
disable-model-invocation: true
---

# Trend Note: Deep Research on Demand

Topic: $ARGUMENTS

## 1. Check the vault first
Search for what already exists on this topic in:
- 00_Inbox/WORLD-INTEL-LIVE.md (daily digests)
- 07_Context/World-Intelligence/ (existing trend notes)
- 02_Areas/World-Intelligence/_Briefings/ (weekly briefings)
If a trend note already exists, this run updates it instead of creating a
duplicate.

## 2. Phase A: deep research
Run one comprehensive query with perplexity_research. Ask for analysis with
citations.

## 3. Phase B: follow-ups
Run 1 to 2 follow-ups with perplexity_search to: verify facts, find the
contrarian point of view, and pull one recent data point.

## 4. Synthesize
- Core claim
- Evidence: 3 to 6 data points, each with a date and URL
- Significance
- Counterarguments
- Open questions
- Vault connections

## 5. Sign-off before writing
Show the user a summary of the note. Do not write anything until they
explicitly approve.

## 6. Write
On approval, write 07_Context/World-Intelligence/[Trend Name].md using
02_Areas/World-Intelligence/_Templates/trend-note-template.md, including the
full frontmatter and every section.
