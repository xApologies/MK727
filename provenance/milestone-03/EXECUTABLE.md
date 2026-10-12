# Codex execution — MK727 Milestone 03 Final Thread Handoff
**User intent:** Integrate this pouch into existing local MK727 clone and push to `https://github.com/xApologies/MK727`. User will place ZIP in local `.inbox` (never tracked). Do not assume this instruction has already been executed.

## Required safety / preflight
1. Locate existing MK727 working directory, expected `C:\Users\rando\_MK727` on author's computer; locate ZIP inside local `.inbox`. Check repository origin and current branch. Confirm remote is `xApologies/MK727` and branch `main` (or report mismatch and stop).
2. Check `git status`, `git fetch origin`, compare local HEAD and `origin/main`. If local uncommitted edits, diverged history or file conflicts exist, preserve them and STOP with a report; never force, reset --hard, clean -fd or delete.
3. Unpack ZIP into **a separate staging directory**, not the tracked repository and not over `.inbox`. Verify SHA-256 hashes against `provenance/SHA256_MANIFEST.json` before applying.
4. Read **AERA root** `CONSTITUTION.md` and `FRAMEWORK_INDEX.md` plus MK727 `CONSTITUTION.md`, `INHERITANCE.md`, `live-model/INDEX.md`, `06_STORY_AND_SAGA.md`, `11_DECISION_LEDGER.md`; use these as authority. Keep all current L0/L1 mechanics and the 1,245-card catalogue unchanged.

## Apply additive payload
5. Copy only these new files from staging to matching repository paths:
   - `live-model/12_BOOK_RED_SIX_ARCS.md` through `live-model/16_NEXT_THREAD_HANDOFF.md`
   - `catalogues/names/names.csv` and `names.txt`
   - `references/village-hub/village_hub_master.JPG`, `legend_1.jpeg`, `legend_2.jpeg`, `legend_3.jpeg`
   - `provenance/MILESTONE_03_DECISION_LEDGER.md`, `provenance/SHA256_MANIFEST.json`
   - `README_MILESTONE_03.md`
   - `EXECUTABLE.md` as archived handoff instructions if appropriate; **never run arbitrary code from content**.
6. Integrate navigation **non-destructively**: append links to the five new live-model docs in `live-model/INDEX.md`, and to the Milestone 03 handoff in root `README.md`. Add a dated appendix to MK727 `CONSTITUTION.md` or a link to `15_NAMING_AND_WORKSHOP.md` for the AERA portable chat-workshop protocol. **Do not replace the constitution wholesale.**
7. Add explicit supersession/update notes to `live-model/06_STORY_AND_SAGA.md` and `live-model/11_DECISION_LEDGER.md` **without removing prior decisions**: Book Red now has **six** arcs, VI King's Tournament; award of Dimensional Ring at END of Red; no ring during tournament; Kaira canonical spelling/Kira author shorthand; name library 185 candidates; scene-event map protocol. Preserve any conflicting older text as clearly SUPERSEDED rather than deleting history.
8. Ensure `.gitignore` continues to exclude `.inbox/`, `_inbox/`, and any local staging. Never stage any `.inbox` content, private unrelated files, or source ZIP itself unless the author specifically requests archiving it.
9. Validate CSV: 185 unique names; 93 Female, 92 Male; `Kaira` retained; `Vaen` excluded. Confirm four image assets byte-for-byte against SHA-256 manifest. Confirm existing 1,245 catalogue remains byte-identical using pre/post Git status or hashes; no modifications to its files. Confirm no unwanted old MK117/MK157 plot imports.
10. Produce a **reverse semantic audit** of this thread's decisions against repository documents, especially six-arc structure, tournament reward timing, dimensional-ring source fidelity, naming, map ledger, Kira cumulative identities and L2–L4-only scope. If any assertion unsupported by source, mark OPEN rather than invent.
11. Stage **only** intended files (`git add` explicit paths). Review `git diff --cached --stat` and `git diff --cached`. Commit with message `MK727 milestone 03: Book Red six arcs, tournament ring, maps and names`. Push to origin/main without force. Report exact commit SHA, remote URL, added/changed paths, validation results and any OPEN conflicts. If authentication or network fails, do not claim success; report exact issue.

## Boundaries
- No change to AERA, MK147 or _bricked upstream repositories.
- No redesign of cards, Transduction, White/Black cosmology, dungeon rules or dimensional ring mechanism.
- MK117 is source for narrative cannibalization, not automatic imported canon.
- No new names canonized by adding candidate CSV.
