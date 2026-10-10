---
name: world-intel-weekly
description: Weekly world intelligence compression. Synthesizes the week's live file into a dated briefing, proposes durable trends for promotion to Context, and resets the live file. Invoke with /world-intel-weekly.
---

# World Intel: Weekly Compression

Turn the week of daily digests into something durable. This skill often runs
unattended on a schedule: never ask the user a question and never wait for
approval. You must NOT write, edit or create anything inside 07_Context/ in
this skill. Promotion to Context always needs the user's explicit approval and
happens only through the two promote skills, never here.

## Step 1: Read everything

- Full read of 00_Inbox/WORLD-INTEL-LIVE.md.
- Scan every existing trend note in 07_Context/World-Intelligence/ to check for
  continuations or contradictions.
- Read the last 3 briefings in 02_Areas/World-Intelligence/_Briefings/ so you
  can tell which patterns have appeared across 2 or more weeks.
- If the live file holds no digests, write a short note saying so to
  .claude/logs/last-weekly.md and stop. Do not reset anything.

## Step 2: Synthesize

Work through the week looking for:
- Top 5 to 7 Signals: ranked by structural significance, not media volume
- Emerging Patterns: two or more signals pointing the same direction. Name each
  as a phrase, not a paragraph.
- Quiet But Important: slow-moving structural things that barely made noise
- Cross-Topic Connections: intersections between different topic areas. This is
  where original insight lives.
- Vault Knowledge Activated: where something this week connects to a book,
  concept or framework already in 07_Context/
- Questions to Track: crisp, specific, unresolved questions worth watching

Explicitly flag where new evidence this week confirms or contradicts an existing
trend note.

## Step 3: Weekly briefing

Create 02_Areas/World-Intelligence/_Briefings/YYYY-MM-DD Weekly Briefing.md
(dated today). It is a structured document with all six synthesis sections
above as headings, in that order, with sources linked throughout.

## Step 4: Propose durable trends for Context

Patterns with staying power, meaning they appear across 2 or more weeks, are
candidates for permanent trend notes in 07_Context/World-Intelligence/.
One-week stories stay in the briefing.

Do not write the notes. Instead, append each candidate to
02_Areas/World-Intelligence/_Pending-Promotions.md with:
- Proposed trend name
- One sharp sentence stating the core claim
- The evidence: dated signals with source URLs, and which weeks it appeared in
- Whether it is a new note or an update to an existing one (name the note)

## Step 5: Reset the live file

Only after confirming the briefing file from Step 3 exists and is non-empty:
overwrite 00_Inbox/WORLD-INTEL-LIVE.md with the clean template from
02_Areas/World-Intelligence/_Templates/live-file-template.md, keeping the
`Last Digest:` date from the old file. If the briefing file is missing, do not
reset.

## Output (always do this last)

Write the full briefing to .claude/logs/last-weekly.md, overwriting the file.
At the very top add a section titled "Awaiting your approval" listing each
proposed promotion in one line, followed by: Reply to the GitHub "Trend promotions" email to approve, or run
/world-intel-promote in the
vault to approve. If any step failed, say so plainly at the top.
