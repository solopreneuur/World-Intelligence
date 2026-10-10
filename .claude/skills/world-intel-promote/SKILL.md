---
name: world-intel-promote
description: Review pending trend promotions with the user and, only on explicit approval, write permanent trend notes to 07_Context/World-Intelligence/. Invoke with /world-intel-promote. Interactive only.
disable-model-invocation: true
---

# World Intel: Promote Trends to Context

1. Read 02_Areas/World-Intelligence/_Pending-Promotions.md. If empty, say so
   and stop.
2. Present each candidate one at a time: name, core claim, evidence. Ask the
   user: approve, edit, or reject. Wait for the answer. Never write without an
   explicit yes.
3. For each approved candidate, create or update the note in
   07_Context/World-Intelligence/[Trend Name].md using
   02_Areas/World-Intelligence/_Templates/trend-note-template.md, including the
   full frontmatter.
4. Remove approved and rejected candidates from the pending file. Leave any the
   user deferred.
