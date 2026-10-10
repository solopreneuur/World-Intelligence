---
name: discuss
description: Talk through items from the World Intel digests with the user, challenge their reasoning, and save their conclusion to the takes file. Invoke with /discuss, optionally followed by a topic. Interactive only.
disable-model-invocation: true
---

# World Intel: Discuss

Topic: $ARGUMENTS

1. Sync. Run `git pull --rebase --autostash` so you are working from the latest
   digests. (--autostash keeps Obsidian's local layout changes from blocking
   the pull.)

2. Load:
   - Today's section of 00_Inbox/WORLD-INTEL-LIVE.md, or the most recent one if
     there is none for today
   - The rest of the week's sections in the same file
   - The trend notes in 07_Context/World-Intelligence/
   - The last 10 entries of 02_Areas/World-Intelligence/My-Takes.md, if it
     exists

3. If a topic is given above, go straight to the matching items. Otherwise list
   today's items as a numbered list of headlines and ask which to discuss.

4. Discuss as a sparring partner:
   - Give the strongest counter-argument to the user's view.
   - Separate what the digests actually show from what the user is inferring.
   - Cite the specific items you rely on (headline and digest date).
   - No flattery. Do not drop a point just because the user pushes back, and do
     say plainly when they are right.
   - Use perplexity_search only if the user asks to check a fact.

5. Save only when the user says so. Draft the take in the user's own words and
   show it before writing. On approval, append it to
   02_Areas/World-Intelligence/My-Takes.md (create the file if it does not
   exist) in this format:

   ## YYYY-MM-DD — [short title]
   **Prompted by:** [headline] ([digest date]) — [link]
   **My take:** [2-4 sentences]
   **What would change my mind:** [1-2 sentences, optional]

   Never edit the digests, briefings or trend notes.

6. Commit only the takes file and push:
   `git add 02_Areas/World-Intelligence/My-Takes.md`, then
   `git commit -m "Take: [short title]"`, then `git push`.
