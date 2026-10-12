"""Read-only M06 integrity checks; carries forward applicable M05 invariants; run with Python 3 from any directory.

--staged checks the complete Git index; --local-bytes checks original working
bytes for protected files. The reverse semantic audit remains a human review.
"""
from pathlib import Path
from urllib.parse import unquote, urlsplit
from collections import Counter
from fractions import Fraction
import argparse
import csv
import hashlib
import io
import json
import re
import runpy
import subprocess

ROOT = Path(__file__).resolve().parents[2]
BASE = '0106e4ebda1dcf9554dd5aaea616c9d05716e603'
ARCHIVE = 'provenance/milestone-06/'
EDITED = set([
    "CONSTITUTION.md",
    "INHERITANCE.md",
    "README.md",
    "live-model/02_WORLD.md",
    "live-model/03_KIRA.md",
    "live-model/05_PROVENANCE.md",
    "live-model/06_STORY_AND_SAGA.md",
    "live-model/09_ARC_ONE.md",
    "live-model/10_SETTLEMENT.md",
    "live-model/11_DECISION_LEDGER.md",
    "live-model/12_BOOK_RED_SIX_ARCS.md",
    "live-model/13_DIMENSIONAL_RING_AND_TOURNAMENT.md",
    "live-model/14_SPATIAL_EVENT_ENGINE.md",
    "live-model/15_NAMING_AND_WORKSHOP.md",
    "live-model/16_NEXT_THREAD_HANDOFF.md",
    "live-model/19_ANTAGONISTS.md",
    "live-model/20_REALMS_AND_STARSCAPE.md",
    "live-model/21_M04_BOOK_RED_EXPANSION.md",
    "live-model/22_CIVILIZATION_AND_WILDS.md",
    "live-model/23_CORRIDORS_AND_PROFESSIONS.md",
    "live-model/24_CARTOGRAPHIC_PROVENANCE.md",
    "live-model/INDEX.md"
])
ADDED = set([
    "live-model/25_CONTINENTAL_POLITIES_AND_TRADE.md",
    "live-model/26_CHAPTER_ONE_EVENT_SEEDS.md",
    "provenance/MILESTONE_06_DECISION_LEDGER.md",
    "provenance/MILESTONE_06_REVERSE_SEMANTIC_AUDIT.md",
    "provenance/MILESTONE_06_SOURCE_REGISTER.md",
    "provenance/milestone-06/EXECUTABLE.md",
    "provenance/milestone-06/PRESERVATION_BASELINE.json",
    "provenance/milestone-06/SHA256_MANIFEST.json",
    "provenance/milestone-06/SOURCE_REGISTER.json",
    "provenance/milestone-06/decisions/M06_WORKSHOP.md",
    "provenance/milestone-06/validate.py",
    "references/m06-cartography/README.md",
    "references/m06-cartography/SOURCE_README.md",
    "references/m06-cartography/atlas_seven_merchant_city_markers.jpeg",
    "references/m06-cartography/atlas_three_kingdom_boundaries.jpeg",
    "references/m06-cartography/atlas_unmarked.jpeg"
])
SPELLING = set([
    "live-model/06_STORY_AND_SAGA.md",
    "live-model/09_ARC_ONE.md",
    "live-model/21_M04_BOOK_RED_EXPANSION.md"
])


def git(*args):
    return subprocess.check_output(['git', *args], cwd=ROOT)


def sha(data):
    return hashlib.sha256(data).hexdigest()


def normalized(data):
    return data.replace(b'\r\n', b'\n')


def section(text, heading):
    start = text.index('## ' + heading + '\n')
    end = text.find('\n## ', start + 3)
    return text[start:end if end >= 0 else len(text)].strip()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--staged', action='store_true')
    ap.add_argument('--local-bytes', action='store_true')
    args = ap.parse_args()
    assert not (args.staged and args.local_bytes), 'Local bytes apply to working files only'
    paths = ('ls-files', '-z') if args.staged else ('ls-files', '-z', '--cached', '--others', '--exclude-standard')
    files = set(git(*paths).decode().strip('\0').split('\0'))
    read = (lambda p: git('show', ':' + p)) if args.staged else (lambda p: (ROOT / p).read_bytes())
    assert not git('ls-files', '-u'), 'Unmerged index entries'
    assert all(not ({'_inbox', '.inbox'} & set(Path(p).parts)) for p in files), 'Inbox staged'
    baseline = json.loads(read(ARCHIVE + 'PRESERVATION_BASELINE.json').decode('utf-8-sig'))
    before = {row['path']: row for row in baseline}
    oldfiles = set(git('ls-tree', '-r', '--name-only', BASE).decode().splitlines())
    assert set(before) == oldfiles and len(oldfiles) == 88
    assert oldfiles <= files, 'Historical file removed'
    assert files - oldfiles == ADDED, f'Unexpected/missing paths: {(files-oldfiles)^ADDED}'
    assert EDITED <= oldfiles
    for path, entry in before.items():
        old = git('show', BASE + ':' + path)
        current = read(path)
        textual = path.endswith(('.md', '.csv', '.txt', '.json', '.py')) or path == '.gitignore'
        candidate = normalized(current) if textual else current
        if path in EDITED:
            expected_old = old.decode('utf-8')
            if path in SPELLING:
                expected_old = re.sub(r'\babeca\b', 'abecca', expected_old)
            assert expected_old.strip() in normalized(current).decode('utf-8'), f'Prior body changed: {path}'
            assert candidate != old and (b'Milestone 06' in current or b'M06' in current), path
        else:
            assert candidate == old, f'Protected content changed: {path}'
            if args.local_bytes:
                assert sha(current) == entry['sha256'] and len(current) == entry['bytes'], f'Protected bytes changed: {path}'

    manifest_bytes = read(ARCHIVE + 'SHA256_MANIFEST.json')
    assert sha(manifest_bytes) == '42598c78e11a3da29009e95f6ef5bedb6c26ee627630ea854a2c1252b2187600', 'Original manifest changed'
    manifest = json.loads(manifest_bytes)
    assert len(manifest) == 6
    for source, entry in manifest.items():
        if source == 'executable.md':
            dest = ARCHIVE + 'EXECUTABLE.md'
        elif source == 'assets/README.md':
            dest = 'references/m06-cartography/SOURCE_README.md'
        elif source.startswith('assets/'):
            dest = source.replace('assets/', 'references/m06-cartography/', 1)
        else:
            dest = ARCHIVE + source
        payload = read(dest)
        assert len(payload) == entry['bytes'] and sha(payload) == entry['sha256'], f'Payload mismatch: {dest}'
    register = json.loads(read(ARCHIVE + 'SOURCE_REGISTER.json'))
    assert register['baseline'] == BASE and len(register['assets']) == 3
    for asset in register['assets']:
        payload = read(asset['path'])
        assert len(payload) == asset['bytes'] and sha(payload) == asset['sha256']
        assert payload.startswith(b'\xff\xd8') and payload.endswith(b'\xff\xd9'), 'JPEG boundary'
    assert len(register['upstream_files']) == 17
    assert len(register['standalone_pdf_wagon_search']) == 19
    assert len(register['additional_markdown_wagon_search']) == 41

    def rows(name):
        return list(csv.DictReader(io.StringIO(read('catalogues/genesis-cards/' + name).decode('utf-8-sig'))))

    bindings, summons, master = [rows(n) for n in ('MK727_BINDINGS_FULL.csv', 'MK727_SUMMONS_FULL.csv', 'MK727_GENESIS_CARD_MASTER_1245.csv')]
    assert [len(bindings), len(summons), len(master)] == [1016, 229, 1245]
    assert len({r['mk727_card_id'] for r in master}) == 1245
    indexed = {r['source_id']: r for r in master}
    assert len(indexed) == 1245
    for row in bindings + summons:
        source_id = row.get('id') or row['entity_id']
        assert all(indexed[source_id].get(k) == v for k, v in row.items()), source_id
        basins = json.loads(row['required_basins'])
        assert len(basins) == len(set(basins)) and set(basins) <= {'Red','Orange','Yellow','Green','Blue','Violet'}
    assert len(rows('MK157_ORIGINAL_BINDINGS.csv')) == 1016
    assert len(rows('MK157_ORIGINAL_SUMMONED_ENTITIES.csv')) == 229
    assert Counter(len(json.loads(r['required_basins'])) for r in bindings) == {2:264, 3:692, 4:60}
    ids = {r['id']: r for r in bindings}
    assert (ids['GF-0011']['name'], json.loads(ids['GF-0011']['required_basins'])) == ('Expanded Genesis Sight', ['Orange','Green','Blue'])
    assert (ids['GF-0019']['name'], json.loads(ids['GF-0019']['required_basins'])) == ('Expanded Transduction Trace', ['Red','Yellow','Green'])
    names = list(csv.DictReader(io.StringIO(read('catalogues/names/names.csv').decode('utf-8-sig'))))
    assert len(names) == 185

    md = {p: read(p).decode('utf-8') for p in files if p.endswith('.md')}
    # Reuse the frozen M04 heading parser without invoking its milestone-specific main.
    anchors = runpy.run_path(str(ROOT / 'provenance/milestone-04/validate.py'))['anchors']
    link_count = 0
    for path, content in md.items():
        assert '\ufffd' not in content and not any(ord(c) < 32 and c not in '\r\n\t' for c in content), path
        assert not re.search(r'^(?:<<<<<<< |=======\s*$|>>>>>>> )', content, re.M), f'Conflict marker: {path}'
        for target in re.findall(r'\[[^\]]*\]\(([^)]+)\)', content):
            target = target.strip('<>')
            parts = urlsplit(target)
            if parts.scheme or target.startswith('//'):
                continue
            local = (ROOT / Path(path).parent / unquote(parts.path)).resolve() if parts.path else ROOT / path
            rel = local.relative_to(ROOT).as_posix()
            assert rel in files or any(p.startswith(rel.rstrip('/') + '/') for p in files), f'Broken link {path}: {target}'
            if parts.fragment and rel in md:
                assert unquote(parts.fragment) in anchors(md[rel]), f'Broken heading {path}: {target}'
            link_count += 1

    def live(name):
        return normalized(read('live-model/' + name + '.md')).decode('utf-8')

    def prior(name):
        return git('show', BASE + ':live-model/' + name + '.md').decode('utf-8')

    arc_one = live('09_ARC_ONE')
    preserved_sections = ['Opening / Chapter 1', 'Collapse / Chapter 2–3',
        'Guard outpost alchemist / Chapter 3', 'Restoration / Chapter 3–4', 'Aftermath / Chapter 5']
    for heading in preserved_sections:
        assert section(arc_one, heading) == section(re.sub(r'\babeca\b', 'abecca', prior('09_ARC_ONE')), heading), heading
    assert section(live('03_KIRA'), 'Collapse, healing, restoration') == section(prior('03_KIRA'), 'Collapse, healing, restoration')
    assert re.sub(r'\babeca\b', 'abecca', prior('21_M04_BOOK_RED_EXPANSION')).strip() in live('21_M04_BOOK_RED_EXPANSION')
    assert section(live('19_ANTAGONISTS'), 'Book emphasis matrix') == section(prior('19_ANTAGONISTS'), 'Book emphasis matrix')
    assert section(live('19_ANTAGONISTS'), 'Environmental pressure and White resolution') == section(prior('19_ANTAGONISTS'), 'Environmental pressure and White resolution')
    ontology = next(p for p in prior('13_DIMENSIONAL_RING_AND_TOURNAMENT').split('\n\n') if p.startswith('**Ring ontology:**'))
    assert ontology in live('13_DIMENSIONAL_RING_AND_TOURNAMENT')
    oldmagic = prior('01_MAGIC').replace('licensed specialist Architect uses sigil workstation', 'licensed Cardsmith uses an Architect/Runesmith-made sigil workstation')
    assert oldmagic.strip() in live('01_MAGIC'), 'L1 changed beyond professional attribution'
    arc_table = section(live('12_BOOK_RED_SIX_ARCS'), 'Milestone 04 current six-arc spine')
    arc_rows = re.findall(r'^\| (I{1,3}|IV|V|VI) \|.*$', arc_table, re.M)
    assert arc_rows == ['I','II','III','IV','V','VI'], 'Six-arc order'
    armor = next(line for line in arc_table.splitlines() if line.startswith('| V |'))
    finale = next(line for line in arc_table.splitlines() if line.startswith('| VI |'))
    assert all(t in armor for t in ('original Armor', 'first third to half', 'black mushroom'))
    assert all(t in finale for t in ('Yellow/fourth', 'after competition', 'Hollowmere', 'first entry'))
    assert 'no ring during I–V or VI competition' in arc_table
    for name in ('03_KIRA','06_STORY_AND_SAGA','09_ARC_ONE','10_SETTLEMENT','11_DECISION_LEDGER',
                 '12_BOOK_RED_SIX_ARCS','13_DIMENSIONAL_RING_AND_TOURNAMENT','14_SPATIAL_EVENT_ENGINE','16_NEXT_THREAD_HANDOFF'):
        content = live(name)
        assert all(t in content for t in ('Hollowmere', 'Green', 'dungeon')), name
    forbidden = ('Mine Hollowmere is only', 'Hollowmere is a Yellow Genesis Mine', 'Hollowmere is not a dungeon')
    assert not any(t in content for path,content in md.items() if path.startswith('live-model/') for t in forbidden)

    civic = live('22_CIVILIZATION_AND_WILDS')
    shares = re.findall(r'^\| (Red|Orange|Yellow|Green|Blue|Violet) \| ([^|]+) \| ([^|]+) \|$', section(civic, 'Districts and landed shares'), re.M)
    assert [r[0] for r in shares] == ['Red','Orange','Yellow','Green','Blue','Violet']
    assert [Fraction(r[1].strip()) for r in shares[:3]] == [Fraction(i,6) for i in range(1,4)]
    assert [Fraction(r[2].strip()) for r in shares] == [Fraction(i,21) for i in range(1,7)]
    assert sum(Fraction(r[1].strip()) for r in shares[:3]) == sum(Fraction(r[2].strip()) for r in shares) == 1
    royals = section(civic, 'Four royal domains')
    assert re.findall(r'^\| (Violet|Orange|Green|Blue) \|', royals, re.M) == ['Violet','Orange','Green','Blue']
    corridor = live('23_CORRIDORS_AND_PROFESSIONS')
    assert 'ONE reusable mobile sigil anchor and ONE Corridor Card' in corridor
    assert 'same anchor' in corridor and 'no second portable anchor' in corridor
    assert 'does not grant automatic control of an existing corridor' in corridor
    assert 'security/encryption, discovery, simultaneous contention and interruption behavior remain OPEN' in corridor

    expected = {f'M06-{i:02d}' for i in range(1,43)}
    for name in ('DECISION_LEDGER', 'REVERSE_SEMANTIC_AUDIT'):
        content = md['provenance/MILESTONE_06_' + name + '.md']
        actual = re.findall(r'^\| (M06-\d\d) \|', content, re.M)
        assert set(actual) == expected and len(actual) == len(expected), name
        assert all(f'[§{i:02d}]' in content for i in range(1,7)), 'Missing source section'
    workshop = md[ARCHIVE + 'decisions/M06_WORKSHOP.md']
    assert re.findall(r'^## (\d\d)\.', workshop, re.M) == ['01','02','03','04','05','06']
    named = {r['name']: r for r in names}
    for name,category,syllables in [('Laira','Female','2'),('Maek','Male','1'),('Raest','Male','1'),('Vael','Male','1')]:
        assert (named[name]['category'], named[name]['syllables'], named[name]['status']) == (category,syllables,'PROPOSED')
    seeds = live('26_CHAPTER_ONE_EVENT_SEEDS')
    proposed = section(seeds, 'Proposed names and verified candidates')
    assert proposed.count('Not author-ratified') == 4
    assert all(token in seeds for token in ('ordinary topical salve','subordinate armorsmith','seven-book rivalry','first Hollowmere entry is Arc VI','no free time or social integration','31-hour day','apothecary → bakery sightline → collision crossing → smithy'))
    for path in SPELLING:
        prefix = normalized(read(path)).decode().split('## Milestone 06',1)[0]
        assert not re.search(r'\babeca\b',prefix), f'Noncanonical current spelling: {path}'
    trade = live('25_CONTINENTAL_POLITIES_AND_TRADE')
    marker_section = section(trade, 'Seven merchant-city markers')
    actual_markers = re.findall(r'^\| (Orange|Red|Yellow|Green|Blue|Violet|White) \| ([^|]+) \|$', marker_section, re.M)
    assert [(c,p.strip()) for c,p in actual_markers] == [('Orange','Western interior'),('Red','Southwest'),('Yellow','South-central'),('Green','Center'),('Blue','Southeast'),('Violet','North'),('White','Eastern interior')]
    assert all(token in trade for token in ('hundreds of square miles','hundreds of miles in radius','23–31','four seeds','five ships is ILLUSTRATIVE','Metal wagons remain OPEN','A toll never guarantees safe passage'))
    assert 'source-recovery gap' in trade, 'Unrecovered wagon source must remain explicit'
    assert all(word in section(trade,'International shipping and cost') for word in ('three cargo ships','five escort ships','ILLUSTRATIVE','seven-month round trip','two-year voyage'))
    assert 'No new map is generated' in live('24_CARTOGRAPHIC_PROVENANCE')
    # Frozen M05 coverage remains available and complete in its unchanged archive.
    for name in ('DECISION_LEDGER','REVERSE_SEMANTIC_AUDIT'):
        assert set(re.findall(r'M05-\d\d',md['provenance/MILESTONE_05_'+name+'.md'])) == {f'M05-{i:02d}' for i in range(1,36)}
    git('diff', '--check')
    if args.staged:
        git('diff', '--cached', '--check')
        changed = set(git('diff', '--cached', '--name-only', BASE).decode().splitlines())
        assert changed == EDITED | ADDED, 'Index differs from verified M06 scope'
    print(json.dumps({
        'mode': 'staged' if args.staged else 'working', 'result': 'PASS',
        'baseline_files_retained':len(before), 'protected_unchanged_files':len(before)-len(EDITED),
        'scoped_existing_files':len(EDITED), 'new_files':len(ADDED), 'manifest_entries':len(manifest),
        'bindings':len(bindings), 'summons':len(summons), 'master_unique_ids':len(indexed), 'names':len(names),
        'markdown_files':len(md), 'local_links_and_fragments':link_count, 'decision_groups':len(expected), 'source_sections':6, 'archived_images':3, 'proposed_names_verified':4,
        'arc_one_sections_preserved_with_spelling_normalized':len(preserved_sections), 'local_byte_snapshot_checked':args.local_bytes,
    }, indent=2))


if __name__ == '__main__':
    main()
