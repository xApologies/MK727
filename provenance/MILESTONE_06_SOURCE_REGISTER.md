# Milestone 06 source and asset register

Date: 2026-10-12 (America/Chicago). Baseline main commit `0106e4ebda1dcf9554dd5aaea616c9d05716e603`, clean and equal to fetched origin/main. All 88 tracked paths inventoried and snapshotted before editing. User-requested scope is the [M06 executable](milestone-06/EXECUTABLE.md) and [six-section workshop](milestone-06/decisions/M06_WORKSHOP.md), not unrelated source-document imperatives.

## Pouch and original images

ZIP SHA-256: `e7a76edf7e5ac135618f7a8ac42bd6ae6dc08943c5134456e052ea56cbcc3a5a`. Original manifest SHA-256: `42598c78e11a3da29009e95f6ef5bedb6c26ee627630ea854a2c1252b2187600`. All six entries match byte count and SHA-256. The executable is archived as uppercase EXECUTABLE.md, workshop under decisions, original asset README as [SOURCE_README.md](../references/m06-cartography/SOURCE_README.md), and three images in [m06-cartography](../references/m06-cartography/README.md). No supplied byte content is changed.

The unmarked atlas and two cropped annotations were visually inspected: the continent above Eastern Whirlpool, two yellow boundary strokes and seven colored dots correspond to the supplied textual description. No coordinates, distances or precise boundaries were extracted. The [image register](../references/m06-cartography/README.md) supplies sizes and hashes; [machine register](milestone-06/SOURCE_REGISTER.json) records dimensions and upstream verification/search metadata. Original pre-M06 map and PDF assets remain unchanged.

## Immutable upstream checks

Complete GitHub main trees (`truncated=false`) resolved to MK147 `ae7c8b406370b752fd5e6f809be0148315294379` and AERA `40e3482b9ea8339ad2c6a9166f3324fa30f42a12`, unchanged from M05. No upstream edits were made. The following relevant documents were fetched at those revisions:

| Owning source | Git blob SHA |
| --- | --- |
| [xApologies/Mk-147/live-model/02_DOMAINS/ELDRIS_DUNGEONS_DOMAI.md](https://github.com/xApologies/Mk-147/blob/ae7c8b406370b752fd5e6f809be0148315294379/live-model/02_DOMAINS/ELDRIS_DUNGEONS_DOMAI.md) | `9c3328f9c0e158ffd5333b1c8ebe40ac1e8efedf` |
| [xApologies/Mk-147/live-model/02_DOMAINS/DIAMONDS_CURRENCY_EQUIPMENT.md](https://github.com/xApologies/Mk-147/blob/ae7c8b406370b752fd5e6f809be0148315294379/live-model/02_DOMAINS/DIAMONDS_CURRENCY_EQUIPMENT.md) | `6776cfb9d0805b09ffb6cf60ae8dc1dbfda1b398` |
| [xApologies/Mk-147/live-model/05_CULTURE/V2_CULTURE_CANON.md](https://github.com/xApologies/Mk-147/blob/ae7c8b406370b752fd5e6f809be0148315294379/live-model/05_CULTURE/V2_CULTURE_CANON.md) | `5d58b35becee583db868e7005e7a5237dfb42fcf` |
| [xApologies/Mk-147/live-model/02_DOMAINS/AGRICULTURE.md](https://github.com/xApologies/Mk-147/blob/ae7c8b406370b752fd5e6f809be0148315294379/live-model/02_DOMAINS/AGRICULTURE.md) | `4165554fc730e1a47c98824a57d64f0d1a83d3f2` |
| [xApologies/Mk-147/live-model/04_SYSTEMS/ARCHITECTS_VELIS.md](https://github.com/xApologies/Mk-147/blob/ae7c8b406370b752fd5e6f809be0148315294379/live-model/04_SYSTEMS/ARCHITECTS_VELIS.md) | `293f53174ccba41c14048e4e1cffe28239ce32a3` |
| [xApologies/Mk-147/live-model/04_SYSTEMS/SIGIL_ENGINEERING.md](https://github.com/xApologies/Mk-147/blob/ae7c8b406370b752fd5e6f809be0148315294379/live-model/04_SYSTEMS/SIGIL_ENGINEERING.md) | `799fc591fe480871704a228362d99debc0426811` |
| [xApologies/AERA/L2/CIVILIZATION.md](https://github.com/xApologies/AERA/blob/40e3482b9ea8339ad2c6a9166f3324fa30f42a12/L2/CIVILIZATION.md) | `ad38b6e0a3ebddd04a3c976b0bd890a8724f0a58` |
| [xApologies/AERA/L2/ENVIRONMENT/03_DUNGEONS.md](https://github.com/xApologies/AERA/blob/40e3482b9ea8339ad2c6a9166f3324fa30f42a12/L2/ENVIRONMENT/03_DUNGEONS.md) | `dd8e10bead09f261bb531b8f4fd5ac5877f86ac6` |
| [xApologies/AERA/L2/INHERITANCE/03_CULTURE_AGRICULTURE_AND_TECH.md](https://github.com/xApologies/AERA/blob/40e3482b9ea8339ad2c6a9166f3324fa30f42a12/L2/INHERITANCE/03_CULTURE_AGRICULTURE_AND_TECH.md) | `2d9dda7d74acb5232ea1abe05c9df3be0ffead5c` |
| [xApologies/AERA/L2/LANGUAGE/AE_AI_NAMING_CONVENTION.md](https://github.com/xApologies/AERA/blob/40e3482b9ea8339ad2c6a9166f3324fa30f42a12/L2/LANGUAGE/AE_AI_NAMING_CONVENTION.md) | `561337655ca6ce7762035b04da1ee12c0c399036` |
| [xApologies/Mk-147/live-model/01_STORY/V2_EXHAUSTIVE_STORY_STATE.md](https://github.com/xApologies/Mk-147/blob/ae7c8b406370b752fd5e6f809be0148315294379/live-model/01_STORY/V2_EXHAUSTIVE_STORY_STATE.md) | `1bc8f662acd05d36694f2ec09469e8a1aba19cfa` |
| [xApologies/Mk-147/live-model/02_WORLD/V2_WORLD_CANON.md](https://github.com/xApologies/Mk-147/blob/ae7c8b406370b752fd5e6f809be0148315294379/live-model/02_WORLD/V2_WORLD_CANON.md) | `ae5021bb418c17039efcfb4079d7ffe645ff3849` |
| [xApologies/Mk-147/live-model/04_SYSTEMS/V2_SYSTEMS_CANON.md](https://github.com/xApologies/Mk-147/blob/ae7c8b406370b752fd5e6f809be0148315294379/live-model/04_SYSTEMS/V2_SYSTEMS_CANON.md) | `763b1b94a7d6dcfda9504998a7049b7d6ba52901` |
| [xApologies/Mk-147/live-model/01_CANON/CULTURE.md](https://github.com/xApologies/Mk-147/blob/ae7c8b406370b752fd5e6f809be0148315294379/live-model/01_CANON/CULTURE.md) | `2b45abedcb1341b9e224aff05f2817d6d491bbf6` |
| [xApologies/Mk-147/live-model/02_WORLD/KINGDOM_SETTLEMENTS.md](https://github.com/xApologies/Mk-147/blob/ae7c8b406370b752fd5e6f809be0148315294379/live-model/02_WORLD/KINGDOM_SETTLEMENTS.md) | `bbe9c86bd09098f2d5fbe10e0f6acf62d0188794` |
| [xApologies/Mk-147/live-model/04_SYSTEMS/ALCHEMY.md](https://github.com/xApologies/Mk-147/blob/ae7c8b406370b752fd5e6f809be0148315294379/live-model/04_SYSTEMS/ALCHEMY.md) | `83a3dc1b7d0ad3cd5869c4cc6db16440afd950e7` |
| [xApologies/Mk-147/live-model/02_DOMAINS/HOSTILE_ORGANIZATIONS.md](https://github.com/xApologies/Mk-147/blob/ae7c8b406370b752fd5e6f809be0148315294379/live-model/02_DOMAINS/HOSTILE_ORGANIZATIONS.md) | `213268cd2dd41fb73143487da88907a34119c834` |

## Inheritance boundaries

MK147/AERA verify R→O→Y→G→B→V dungeon stratification, effective confinement and separate support towns. M06 locally supplies Hollowmere's Green endpoint, separate staging village and WORKING measurements. The 31-hour day appears in MK147 world canon; a 31-hour illustrative overwork context does not adopt its whole calendar or resolve its nine-day month-total discrepancy.

Architect velis growth/nutrient uptake, alchemical growing media, material-growing physical sigil arrays and dungeon participation culture support the local trade directions. AERA explicitly leaves government/economy/professions as world choices. M06's polity structures, named commodity spelling/botanical concept, extraction models and maritime examples are author decisions, not claims that all AERA settings follow them.

Current MK727 Genesis Cards override incompatible MK147 personal Binding Circle/Nyx/helkir story causality. No Age-of-Knowledge chronology, diamond density ladder, fixed-ring-radius override, specific pirate hierarchy, volcanic island geography or old drug methods are adopted. The existing M04 antagonist matrix remains foreground emphasis, not an activity start date.

## Naming lookup

The unchanged CSV contains exact entries Female/Laira/2/PROPOSED, Male/Maek/1/PROPOSED, Male/Raest/1/PROPOSED and Male/Vael/1/PROPOSED. Their suggested roles are not approved assignments. The AERA naming source supports optional tendencies and author approval; no forced pattern or new names are required. Current manuscript Kaira and lowercase abecca take precedence over historical Kira shorthand and abeca source spelling.

## Wagon search limits

All 54 MK147 Markdown files were reviewed or keyword-searched at the pinned commit: 13 relevant files read above and 41 additional files searched. Nineteen standalone PDFs directly under live-model/05_SOURCES were downloaded read-only, Git blob hashes verified and all extracted pages searched for wagon/fifth-wheel terms; no design match. PDF parser warnings about unused object offsets did not prevent extraction. The original PDFs were not rewritten or vendored into MK727. The machine register lists each searched file/hash/page count.

Inventories of Genesis(1).zip and MASTER(3).zip were inspected; they contain language/math/recovery packages rather than a named wagon document. Nested document contents were not searched. No global absence claim follows this bounded search. The wagon reference remains unrecovered and material design remains OPEN; provide the original source pointer before deciding construction. Search-only PDFs supply no new MK727 content authority.

## Cartographic limits and remaining differences

M06 resolves atlas availability but not the separate original geographic/climate drawings or four-color Crown-domain overlay. Continental boundary strokes and merchant dots must not be confused with royal-domain capital X marks or the old purple-X hub/mining-X conventions. Captions such as polar Violet Realm, biome colors, an Earth-size comparison and an approximate scale remain image content; they neither supersede written basin/realm distinctions nor establish physical measurements. Atlas bytes are preserved without corrective painting.

Merchant square-mile area versus mile-radius alternatives remain explicitly unresolved. Hollowmere measurements remain WORKING and unverified against the preserved master. GF-0011/GF-0019 description mismatches and inherited ring-radius wording differences remain intentionally untouched. These are distinguished from Git conflicts and from author-reserved OPEN details in the [reverse audit](MILESTONE_06_REVERSE_SEMANTIC_AUDIT.md).
