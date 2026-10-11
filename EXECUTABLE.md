# Codex execution — MK727 initial publication

User instruction: **Unpack the ZIP into the local `_MK727` working directory and execute this file.** The local path shown by the user is `C:\Users\rando\_MK727`; do not assume that path on a different machine.

1. Confirm the working directory is `_MK727` and that `.inbox/` exists. **Never delete, move, commit, or alter `.inbox/`**. If the ZIP was unpacked inside `.inbox`, copy only package files to repository root; leave inbox intact.
2. Inspect `git status`, `git remote -v`, and existing files. If this is not already a Git repository, run `git init -b main`. If Git is already initialized, preserve its history, branch and files. Do not overwrite unrelated user work.
3. Set `origin` to `https://github.com/xApologies/MK727.git` only if absent; if a different origin exists, stop and report instead of overwriting. `git fetch origin` when remote exists; if remote main contains commits, reconcile them non-destructively before publishing. Never force push.
4. Copy package contents (excluding `EXECUTABLE.md` if desired; retaining it as deployment provenance is acceptable) into repository root. Ensure `.gitignore` excludes `.inbox/`.
5. Validate with Python standard library: count 1,016 records in `MK727_BINDINGS_FULL.csv`, 229 in `MK727_SUMMONS_FULL.csv`, 1,245 in `MK727_GENESIS_CARD_MASTER_1245.csv`; check unique IDs; check all nine Prime entries have exactly three valid R–V basin names; verify no `/.inbox/` path is staged. Validate source snapshots and full descriptions remain present. If any check fails, STOP before commit.
6. Stage explicit project files, never `.inbox/`. Example: `git add README.md CONSTITUTION.md INHERITANCE.md .gitignore EXECUTABLE.md live-model catalogues references`. Verify `git diff --cached --stat` and `git status --short`.
7. Commit `MK727: initialize Genesis Card live model and 1245 shaping catalogue`. Push `main` to origin after verifying remote branch status. If remote has unrelated history or conflicts, STOP and ask rather than forcing.
8. Report actual commit SHA, pushed branch, full file list, counts, and any unresolved upstream inheritance items. Do not claim success until remote publication is confirmed.

Do not modify AERA, Mk-147, _bricked, or MK157. Do not invent extra lore or perform story rewriting. No GitHub secret/token is needed in files; rely on the user's existing Git credentials.
