# MK727 Milestone 02 deployment report

Deployment date: 2026-10-11 (America/Chicago).

## Repository and package

- Repository: https://github.com/xApologies/MK727.git
- Intended remote branch: `origin/main` (`refs/heads/main`).
- Starting commit: `8ed752f0d12f2dd05e264000a9e1c2daf60a2f57`. Local `main` was clean and matched fetched `origin/main` (0 ahead, 0 behind).
- Package: `_inbox/MK727_MILESTONE_02_CODEX_POUCH.zip`.
- Package SHA-256: `a9ea5198c38d3ea9758b067f3517aa8c16daced529bfaf78f6a72eee91e8f016`.
- The actual inbox is `_inbox`, although the package calls it `.inbox`. Both spellings are already ignored. All existing inbox files were hashed before and after; their names and bytes are unchanged.
- Applied the 16 supplied files exactly as packaged: seven replacements including the deployment instructions, and nine additions. This report and a scoped `.gitattributes` rule are two additional deployment files (18 changed files total).
- Temporary extraction and validation materials are ignored and excluded from the commit.

## Catalogue validation

| File | Records | ID validation |
| --- | ---: | --- |
| `MK727_BINDINGS_FULL.csv` | 1,016 | Nonempty and unique |
| `MK727_SUMMONS_FULL.csv` | 229 | Nonempty and unique |
| `MK727_GENESIS_CARD_MASTER_1245.csv` | 1,245 | Nonempty and unique |
| `MK157_ORIGINAL_BINDINGS.csv` | 1,016 | Nonempty and unique |
| `MK157_ORIGINAL_SUMMONED_ENTITIES.csv` | 229 | Nonempty and unique |

- All CSV rows are structurally complete. All 1,245 master records match every corresponding field of their Binding or Summon record, including full descriptions, record type and source ID.
- Every current card has a valid, nonempty set of distinct Red-through-Violet basin names. Binding distribution remains 264 two-basin, 692 three-basin and 60 four-basin records.
- All nine Prime IDs match the decision JSON and have exactly three valid, distinct basins.
- All catalogue files, both original MK157 snapshots and the Prime decision JSON have identical before/after SHA-256 hashes. Nothing was regenerated.

All paths in the following table are under `catalogues/genesis-cards/`. Each value was measured both before and after copying.

| File | SHA-256 before = SHA-256 after |
| --- | --- |
| `MK157_ORIGINAL_BINDINGS.csv` | `caa71867ee138af97869e08ca2793b6777b4b9171cb86703c316ca92dd9bf089` |
| `MK157_ORIGINAL_SUMMONED_ENTITIES.csv` | `abaf139cc6f8bdb7bf0ad9421f7d21c5278caa1b3d3ac72cdbef4da768f5d857` |
| `MK727_BINDINGS_FULL.csv` | `c9b0da644369365f50bb57fa88a500bf8a0960e04c084407e82ab1ec10b9d41b` |
| `MK727_GENESIS_CARD_MASTER_1245.csv` | `5a252433c88582a549038bdf45b8b64ee6af1cadd42894fd4d2a92d4ccf3b003` |
| `MK727_SUMMONS_FULL.csv` | `87071a3c44e7c3beba0a8cf96645963427927771b2030c2046781932ab44a85d` |
| `PRIME_BASIN_DECISIONS.json` | `1a6533ce8aeedb60539eeeb95b8eab406b6dcc6c1a528b665a671f6edc78f499` |

## Applied files

| Action | Path |
| --- | --- |
| Replace | `CONSTITUTION.md` |
| Replace | `EXECUTABLE.md` |
| Replace | `INHERITANCE.md` |
| Replace | `README.md` |
| Replace | `live-model/03_KIRA.md` |
| Replace | `live-model/05_PROVENANCE.md` |
| Replace | `live-model/INDEX.md` |
| Add | `AUDIT_MILESTONE_02.md` |
| Add | `live-model/06_STORY_AND_SAGA.md` |
| Add | `live-model/07_BLACK_CARDS.md` |
| Add | `live-model/08_EDUCATION_PROFESSIONS.md` |
| Add | `live-model/09_ARC_ONE.md` |
| Add | `live-model/10_SETTLEMENT.md` |
| Add | `live-model/11_DECISION_LEDGER.md` |
| Add | `references/MK117/MK117_Book1_Arc_Outline.pdf` |
| Add | `references/MK117/MK117_Chapters_1_5_Master_Workup.pdf` |
| Add | `MILESTONE_02_DEPLOYMENT_REPORT.md` |
| Add | `.gitattributes` |

Preserved byte-for-byte: `live-model/01_MAGIC.md`, `live-model/02_WORLD.md`, `live-model/04_CATALOGUE.md`, `AUDIT.md`, `.gitignore`, the agriculture PDF, and every catalogue file. No unrelated files were overwritten.

## Milestone acceptance checks

- Revised biography: licensed Cardsmith mother; death at Kira age 15; smithy ages 16-23 / seven years; three inherited books; one ordinary Fireball Card; no Black crystal; six consumed R-V crystals and an additional consumed exceptional White catalyst.
- Black Cards: exactly five foundational systems (Armor of the Abyss, Continuous Spatial Resolution, Genesis Orbs, Halo, Domain). Sixth slot remains OPEN; mixed ordinary/Black concurrency remains OPEN.
- Arc One: smith-owned donkey/cart, travel without the old apprentice, ordinary emergency healing distinct from restoration, retained scars.
- Professions: Cardsmith apprenticeship, manual chainmail craft, robe designer/business owner, educated Cardsmith/Architect, Black Card researcher and independent aithren adventurer are all retained.
- All 19 supplied/existing Markdown documents, including this report, decode as UTF-8 without replacement characters or invalid controls. All 97 checked file references resolve using the package's document-relative or repository-relative conventions; actual local Markdown links were also checked.
- Git initially classified the ASCII-encoded reference PDFs as text, reporting whitespace and potential LF-to-CRLF conversion. The scoped `/references/MK117/*.pdf binary` rule prevents text normalization and text diffs for these archives. Their staged bytes are checked against the original package before committing.
- `git diff --check` and `git diff --cached --check` must both pass before committing. Only the explicit milestone files, this report and `.gitattributes` may be staged; inbox and temporary materials are excluded.

## Source PDF checks

| Archive | Pages | SHA-256 |
| --- | ---: | --- |
| `references/MK117/MK117_Book1_Arc_Outline.pdf` | 8 | `4fefd9bdba03a79d537f713665698699bbf60176099a983dde5490ebf3e45fad` |
| `references/MK117/MK117_Chapters_1_5_Master_Workup.pdf` | 7 | `f7897d1cd08b81d8a1c663cfd5516578b364dcb75a4fe2e64948f8ec85bcf547` |

Both PDFs parse strictly with pypdf, are unencrypted, and yield nonempty text on every page. All 15 pages rendered with Poppler and were visually reviewed in contact sheets. Poppler emitted display-font configuration warnings for Symbol/ArialUnicode; the rendered archive text and layout were readable. The PDFs remain exact package copies.

## Conflicts and unresolved source decisions

- No Git conflicts or unrelated local edits were present during application.
- The MK117 archives use Enix, an accompanying apprentice, a Black crystal/stabilizer, and a healer/academy/hospital career. Those archived details remain reference material; the explicit MK727 biography and decision ledger supersede them.
- The MK117 sources disagree on first Fireball acquisition: the short workup already gives the character a card, while the longer outline describes a later first purchase. MK727 starts with one card; its exact catalogue ID and basins remain OPEN. No candidate was silently selected.
- Uploaded maps mentioned by the new model are absent from this package and the tracked repository. Route geometry, coordinates and map-derived distances cannot be verified here and remain unresolved.
- Preserved First Light `01_MAGIC.md` describes ordinary chromatic occupancy. The new constitution and Black Card file add Black-specific concurrency; their combined ordinary/Black limit remains OPEN, with no extrapolated total.
- The five Black-system inheritance claims are supplied by this milestone; an independently pinned MK157 source for them is not bundled. Upstream AERA, _bricked, Mk-147 and historical source Git SHA pins remain OPEN.
- Other open items remain as supplied: sixth Black Card; Black-compatible manufacture and first Armor recipe/timing; Domai classification of the collapse; donkey/cart fate; former workshop ownership; exact potion ingredients/prices; academy chronology; companion identities; later saga details; Halo throughput/fatigue values remain WORKING.

## Commit and publication receipt

Milestone content commit: `abc2354753637b843f77bc6513faba99b75b1acd`.

Commit message: `MK727: milestone 02 story and Black Card live model`.

The content commit contains the complete milestone and validation report. This report-only follow-up records its actual SHA without changing the live model, catalogue or source archives.

Publication target: `origin/main`. Publication follows the report-only commit; the final deployment response records the remotely verified result. To verify the current published tip, compare `git rev-parse HEAD` with `git ls-remote origin refs/heads/main`.

The commit containing this report cannot embed its own SHA. Its publication commit can be resolved with `git log -1 --format=%H -- MILESTONE_02_DEPLOYMENT_REPORT.md`.
