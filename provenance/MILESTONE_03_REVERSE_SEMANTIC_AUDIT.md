# Milestone 03 reverse semantic audit

Date: 2026-10-11 (America/Chicago). Target: `https://github.com/xApologies/MK727.git`, `main`.
Baseline: `5fae1259425d2db75deae0b19445434c524d3325`. Local main was clean and matched fetched origin/main before applying.

## Audit scope and result

All 15 supplied decision IDs are represented in the repository, with source boundaries and OPEN items retained. This is a reverse comparison from the user-authorized pouch decisions to resulting documents, not merely a file or Git-status check. The original off-chat author discussion is not available here; its claims are evaluated as the supplied milestone decisions rather than independently witnessed conversation history.

Existing files are preserved: 25 tracked files remain byte-for-byte unchanged; five receive appendices only, with their complete original byte sequences retained. The additions stay within MK727 narrative, naming, map provenance and workflow. No upstream repository, card mechanic, dungeon rule or ring mechanism was edited.

## Decision coverage

| Decision | Result | Reverse comparison / retained boundary | Repository evidence |
| --- | --- | --- | --- |
| M03-01 | PASS | Current work is L2-L4. The existing L0/L1 implementation, full card catalogue and AERA sources remain unchanged. | [Document](../CONSTITUTION.md) |
| M03-02 | PASS / qualified | Exactly six arcs, I-VI, in the supplied order. Arc IV does not silently promote the WORKING first Armor manufacturing placement into a fixed scene. | [Document](../live-model/12_BOOK_RED_SIX_ARCS.md) |
| M03-03 | PASS | King's Tournament is Arc VI and the Book Red finale. | [Document](../live-model/12_BOOK_RED_SIX_ARCS.md) |
| M03-04 | PASS / OPEN values | Ring reward is an MK727 story choice in the authorized pouch. Quality, precise placing and prize details remain OPEN; no unsupported tournament result was inferred. | [Document](../live-model/13_DIMENSIONAL_RING_AND_TOURNAMENT.md) |
| M03-05 | PASS | No ring in I-V or during VI competition. Conventional gear remains necessary; award is after competition at the end of Red, available in Orange-White. | [Document](../live-model/12_BOOK_RED_SIX_ARCS.md) |
| M03-06 | PASS / source verified | AERA and its 20-page master agree on recursive topology, conscious selection, inheritance reassignment, both operation sequences, adjustable projection reach and learned retrieval. No pocket dimension, inventory UI or capacity formula introduced. | [Document](../live-model/13_DIMENSIONAL_RING_AND_TOURNAMENT.md) |
| M03-07 | PASS / source verified | MK147 line 16 supports bottom-token-surface racing, V6/B5/G4/Y3/O2/R1 scoring, qualification-regional-top-six-finals progression. Purple Region wording remains OPEN. | [Document](../live-model/13_DIMENSIONAL_RING_AND_TOURNAMENT.md) |
| M03-08 | PASS / authored scale | All four source images are intact and decodable; visual inspection confirms numbered legend entries 1-40. Half-mile square is the supplied author decision, not a scale inferred from pixels. Exact calibration and cropped legend expansions remain OPEN. | [Document](../live-model/14_SPATIAL_EVENT_ENGINE.md) |
| M03-09 | PASS | Map protocol records event provenance, occupancy, independent schedules, routes, timing, witnesses and consequences. No invented scene rows, routes or overlays. | [Document](../live-model/14_SPATIAL_EVENT_ENGINE.md) |
| M03-10 | PASS | Kaira is canonical manuscript spelling; Kira remains author shorthand. Historical filenames and text are retained with cumulative clarification. | [Document](../live-model/15_NAMING_AND_WORKSHOP.md) |
| M03-11 | PASS | CSV and text agree on 185 unique candidates: 93 Female / 92 Male; all CSV rows PROPOSED, Kaira retained, Vaen absent. Optional AE/AI tendencies match AERA. No other character assignments are implied. | [Document](../catalogues/names/names.csv) |
| M03-12 | PASS | Pen develops requested narrative and may suggest names, Ink retains final canon authority, Page audits. These are collaboration roles, not separate autonomous agents. | [Document](../CONSTITUTION.md) |
| M03-13 | PASS | Craftswoman, robe designer/business owner, Cardsmith/Architect, Black researcher and adventurer identities accumulate. Aithren entry is to adventure; existing biography and profession files remain byte-identical. | [Document](../live-model/08_EDUCATION_PROFESSIONS.md) |
| M03-14 | PASS / supersession explicit | The older five-part summary is preserved and labeled SUPERSEDED as a complete arc count. Any pre-award ring use is superseded; prior seven-book and five-system decisions remain. | [Document](../live-model/06_STORY_AND_SAGA.md) |
| M03-15 | OPEN / retained | Ring quality/result, exact pixel ratio/routes, scene timing and unassigned character names remain OPEN. Earlier Fireball ID, mixed concurrency, sixth Black Card, Armor recipe, donkey/cart fate and workshop disposition also remain OPEN. | [Document](../live-model/11_DECISION_LEDGER.md) |

## Owning-source verification

- AERA local checkout was clean at `40e3482b9ea8339ad2c6a9166f3324fa30f42a12`; GitHub main returned the same SHA. Read [root constitution](https://github.com/xApologies/AERA/blob/40e3482b9ea8339ad2c6a9166f3324fa30f42a12/CONSTITUTION.md), [framework index](https://github.com/xApologies/AERA/blob/40e3482b9ea8339ad2c6a9166f3324fa30f42a12/FRAMEWORK_INDEX.md), [dimensional rings](https://github.com/xApologies/AERA/blob/40e3482b9ea8339ad2c6a9166f3324fa30f42a12/L2/TECHNOLOGY/DIMENSIONAL_RINGS.md), and [optional naming convention](https://github.com/xApologies/AERA/blob/40e3482b9ea8339ad2c6a9166f3324fa30f42a12/L2/LANGUAGE/AE_AI_NAMING_CONVENTION.md).
- MK147 local checkout was clean at `ae7c8b406370b752fd5e6f809be0148315294379`; GitHub main returned the same SHA. Read [V2_WORLD_CANON.md, Dungeons](https://github.com/xApologies/Mk-147/blob/ae7c8b406370b752fd5e6f809be0148315294379/live-model/02_WORLD/V2_WORLD_CANON.md#dungeons).
- The [ring master PDF](https://github.com/xApologies/AERA/blob/40e3482b9ea8339ad2c6a9166f3324fa30f42a12/provenance/technology-v0.6.0/sources/DIMENSIONAL_RING_MASTER.pdf) has 20 pages and SHA-256 `074080af01829b969defe2269c0b14f064bce9a1de9f8c4bb3bde5ee7ffd19b2`, matching the AERA source register. Reviewed its identity/conservation, storage/retrieval, radius, recognition, logistics and civilization passages. Adjustable reach examples are not a storage-volume or capacity law.
- Source revisions above are evidence for this audit, not new blanket adoption of all upstream history. Other inherited-source revision pins remain unresolved.

| Source file | SHA-256 of reviewed bytes |
| --- | --- |
| `AERA/CONSTITUTION.md` | `5345121d04f3e5d6df738d93d198bdca3e3f9141f37c1d0903cabd321494a8de` |
| `AERA/FRAMEWORK_INDEX.md` | `4396888513d8a6654d46e8733747c38e2dfd0a67835c7597d55ce530eea862a3` |
| `AERA/L2/TECHNOLOGY/DIMENSIONAL_RINGS.md` | `9467d68d00927596f53ce136ff333baf9ab921130631f340c981692518a6ba61` |
| `AERA/L2/LANGUAGE/AE_AI_NAMING_CONVENTION.md` | `4f2dc32af41a3a1916ecf30025ea33d12d4405eae947221bdb8389c3e93888d6` |
| `AERA/provenance/technology-v0.6.0/sources/DIMENSIONAL_RING_MASTER.pdf` | `074080af01829b969defe2269c0b14f064bce9a1de9f8c4bb3bde5ee7ffd19b2` |
| `Mk-147/live-model/02_WORLD/V2_WORLD_CANON.md` | `e8a65523b2f0676754c40507c143c8aa022a5bb32cf2f975c9489b305116d00a` |

## Wording qualifications and unsupported claims

1. **First Armor placement:** the six-arc sequence is established; the exact Blackstone acquisition/manufacture event remains WORKING/OPEN under Milestone 02 and the new handoff. The cumulative saga/decision appendices make that distinction explicit.
2. **Scarring:** the new handoff says emergency healing "causes scarring." Existing `03_KIRA.md` and `09_ARC_ONE.md` establish healed injuries that retain scars, not an independent harmful potion effect. That stronger causal assertion is unsupported/OPEN, and the cumulative ledger preserves the earlier meaning. The supplied handoff itself is retained verbatim as provenance.
3. **Map evidence:** the source images visibly supply numbered entries 1-40, but some labels are truncated (including 8 and 18). Expanded wording is OPEN. The half-mile-square scale is an author decision in the pouch; no pixel-to-foot ratio, exact route, named scene location or travel time was invented. Map availability resolves the previous missing-assets issue, not all geographic questions.
4. **Historical cleanup:** the delivered 185-name pool and exclusion of Vaen are verified. The earlier 200-name list and full list of 15 removals are absent, so that historical cleanup cannot be independently reproduced. Candidate inclusion creates no new named character. The existing Kaira spelling remains canonical despite its pool row retaining PROPOSED candidate metadata.
5. **Workshop scope:** AERA documents the roles and repository workflow but explicitly defers a complete public pedagogy. The new constitution appendix adopts the documented protocol without claiming that deferred material is complete.

## Preservation and package validation

- ZIP SHA-256: `e39aae45cc7101519ca8fc4c603637ce90ea742cc567891908e8cf95c6554dfb`. All 14 listed manifest entries match both SHA-256 and byte count before application. The manifest excludes itself; its exact delivered bytes are also retained.
- Fifteen payload files are copied without byte changes. The incoming `EXECUTABLE.md` is archived at [provenance/milestone-03/EXECUTABLE.md](milestone-03/EXECUTABLE.md); the prior root executable remains intact. Manifest paths describe the original pouch layout, so its executable entry is checked against that archived copy.
- No inbox contents, source ZIP or staging files are staged. The actual inbox is `_inbox`; both `_inbox/` and `.inbox/` remain excluded by the existing `.gitignore`. Staging is outside the repository.
- Name CSV: 185 case-insensitively unique names, 93 Female and 92 Male, all PROPOSED. Kaira is present and Vaen absent. The text library agrees with CSV category order and names.
- Genesis catalogue: 1,016 Bindings, 229 Summons and 1,245 unique master IDs. Every master record matches every source field; full descriptions remain present. Both MK157 snapshots retain 1,016 and 229 records. All basin arrays are valid; all nine Primes retain their three assignments; Binding basin distribution stays 264 two-basin, 692 three-basin and 60 four-basin cards.
- All existing catalogue files and source snapshots retain identical before/after hashes. Existing live-model files 01-05 and 07-10 are byte-identical. Files 06, 11 and INDEX receive appendices only. README and CONSTITUTION also receive appendices only. The prior root executable, audits, reports, Git configuration files and source PDFs are unchanged.
- New and existing Markdown are checked for valid UTF-8 and replacement/control characters; local Markdown links resolve. Working-tree and staged whitespace checks, staged-path allowlist and exact staged payload bytes are required before commit. Images are decoded and visually inspected without alteration.

All catalogue paths below are relative to `catalogues/genesis-cards/`. Each hash was measured before and after application.

| File | SHA-256 before = SHA-256 after |
| --- | --- |
| `MK157_ORIGINAL_BINDINGS.csv` | `caa71867ee138af97869e08ca2793b6777b4b9171cb86703c316ca92dd9bf089` |
| `MK157_ORIGINAL_SUMMONED_ENTITIES.csv` | `abaf139cc6f8bdb7bf0ad9421f7d21c5278caa1b3d3ac72cdbef4da768f5d857` |
| `MK727_BINDINGS_FULL.csv` | `c9b0da644369365f50bb57fa88a500bf8a0960e04c084407e82ab1ec10b9d41b` |
| `MK727_GENESIS_CARD_MASTER_1245.csv` | `5a252433c88582a549038bdf45b8b64ee6af1cadd42894fd4d2a92d4ccf3b003` |
| `MK727_SUMMONS_FULL.csv` | `87071a3c44e7c3beba0a8cf96645963427927771b2030c2046781932ab44a85d` |
| `PRIME_BASIN_DECISIONS.json` | `1a6533ce8aeedb60539eeeb95b8eab406b6dcc6c1a528b665a671f6edc78f499` |

## Map asset preservation

| Asset | Pixels | SHA-256 |
| --- | --- | --- |
| [legend_1.jpeg](../references/village-hub/legend_1.jpeg) | 582 x 2195 | `c454c5158813e8d15716012fa553c028fe7ee87c1a833ce6f3fdc76b4bcba5c1` |
| [legend_2.jpeg](../references/village-hub/legend_2.jpeg) | 557 x 2094 | `31ff78f1d15c1afc8451e783ea01915bb344f4c238b4e4fd4a02b3a396142323` |
| [legend_3.jpeg](../references/village-hub/legend_3.jpeg) | 556 x 1407 | `f8a0bd8481d649d5c3bb7201f1f18e8fed4a5814ff690bea97f9c1ae479a4874` |
| [village_hub_master.JPG](../references/village-hub/village_hub_master.JPG) | 6144 x 6144 | `a5e2e9b7fcfa69af7b75b21eb29a32a5e7f11745e7c4cdb81c1f9afb43641d63` |

## Added and updated paths

| Action | Path |
| --- | --- |
| Append only | `README.md` |
| Append only | `CONSTITUTION.md` |
| Append only | `live-model/INDEX.md` |
| Append only | `live-model/06_STORY_AND_SAGA.md` |
| Append only | `live-model/11_DECISION_LEDGER.md` |
| Add exact payload | `provenance/milestone-03/EXECUTABLE.md` |
| Add exact payload | `README_MILESTONE_03.md` |
| Add exact payload | `catalogues/names/names.csv` |
| Add exact payload | `catalogues/names/names.txt` |
| Add exact payload | `live-model/12_BOOK_RED_SIX_ARCS.md` |
| Add exact payload | `live-model/13_DIMENSIONAL_RING_AND_TOURNAMENT.md` |
| Add exact payload | `live-model/14_SPATIAL_EVENT_ENGINE.md` |
| Add exact payload | `live-model/15_NAMING_AND_WORKSHOP.md` |
| Add exact payload | `live-model/16_NEXT_THREAD_HANDOFF.md` |
| Add exact payload | `provenance/MILESTONE_03_DECISION_LEDGER.md` |
| Add exact payload | `provenance/SHA256_MANIFEST.json` |
| Add exact payload | `references/village-hub/legend_1.jpeg` |
| Add exact payload | `references/village-hub/legend_2.jpeg` |
| Add exact payload | `references/village-hub/legend_3.jpeg` |
| Add exact payload | `references/village-hub/village_hub_master.JPG` |
| Add audit | `provenance/MILESTONE_03_REVERSE_SEMANTIC_AUDIT.md` |

## Publication verification

The milestone commit uses `MK727 milestone 03: Book Red six arcs, tournament ring, maps and names`. This audit is included in that commit. The final deployment response supplies its exact SHA after origin/main is independently checked; this file makes no premature publication claim.
