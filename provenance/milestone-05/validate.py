"""Read-only M05 integrity checks; run with Python 3 from any directory.

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
BASE = 'ce0c105c7e93b92869addaf6aaebf9d25285974e'
ARCHIVE = 'provenance/milestone-05/'
EDITED = {'CONSTITUTION.md', 'INHERITANCE.md', 'README.md', 'live-model/INDEX.md'} | {
    'live-model/' + name for name in (
        '01_MAGIC.md', '02_WORLD.md', '03_KIRA.md', '05_PROVENANCE.md',
        '06_STORY_AND_SAGA.md', '08_EDUCATION_PROFESSIONS.md', '09_ARC_ONE.md',
        '10_SETTLEMENT.md', '11_DECISION_LEDGER.md', '12_BOOK_RED_SIX_ARCS.md',
        '13_DIMENSIONAL_RING_AND_TOURNAMENT.md', '14_SPATIAL_EVENT_ENGINE.md',
        '16_NEXT_THREAD_HANDOFF.md', '18_CARDSMITHING_WORKSPACE.md',
        '19_ANTAGONISTS.md', '20_REALMS_AND_STARSCAPE.md', '21_M04_BOOK_RED_EXPANSION.md')
}
ADDED = {
    'live-model/22_CIVILIZATION_AND_WILDS.md',
    'live-model/23_CORRIDORS_AND_PROFESSIONS.md',
    'live-model/24_CARTOGRAPHIC_PROVENANCE.md',
    'provenance/MILESTONE_05_DECISION_LEDGER.md',
    'provenance/MILESTONE_05_SOURCE_REGISTER.md',
    'provenance/MILESTONE_05_REVERSE_SEMANTIC_AUDIT.md',
} | {ARCHIVE + name for name in (
    'EXECUTABLE.md', 'SHA256_MANIFEST.json', 'PRESERVATION_BASELINE.json', 'validate.py',
    'decisions/01_HOLLOWMERE.md', 'decisions/02_CIVILIZATION.md',
    'decisions/03_CORRIDORS.md', 'decisions/04_MAP_AND_UNDERWORLD.md')}


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
    assert set(before) == oldfiles and len(oldfiles) == 74
    assert oldfiles <= files, 'Historical file removed'
    assert files - oldfiles == ADDED, f'Unexpected/missing paths: {(files-oldfiles)^ADDED}'
    assert EDITED <= oldfiles
    for path, entry in before.items():
        old = git('show', BASE + ':' + path)
        current = read(path)
        textual = path.endswith(('.md', '.csv', '.txt', '.json', '.py')) or path == '.gitignore'
        candidate = normalized(current) if textual else current
        if path in EDITED:
            assert candidate != old and (b'Milestone 05' in current or b'M05' in current), path
        else:
            assert candidate == old, f'Protected content changed: {path}'
            if args.local_bytes:
                assert sha(current) == entry['sha256'] and len(current) == entry['bytes'], f'Protected bytes changed: {path}'

    manifest_bytes = read(ARCHIVE + 'SHA256_MANIFEST.json')
    assert sha(manifest_bytes) == '3f09b4fdcf9de4171d93c6e9935ad27b5aaf35a0e8b59d11766535a8f37ca2de', 'Original manifest changed'
    manifest = json.loads(manifest_bytes)
    assert len(manifest['files']) == 5
    for entry in manifest['files']:
        dest = ARCHIVE + ('EXECUTABLE.md' if entry['path'] == 'executable.md' else entry['path'])
        payload = read(dest)
        assert len(payload) == entry['bytes'] and sha(payload) == entry['sha256'], f'Payload mismatch: {dest}'

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
        assert section(arc_one, heading) == section(prior('09_ARC_ONE'), heading), heading
    assert section(live('03_KIRA'), 'Collapse, healing, restoration') == section(prior('03_KIRA'), 'Collapse, healing, restoration')
    assert prior('21_M04_BOOK_RED_EXPANSION').strip() in live('21_M04_BOOK_RED_EXPANSION')
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

    expected = {f'M05-{i:02d}' for i in range(1,36)}
    for name in ('DECISION_LEDGER', 'REVERSE_SEMANTIC_AUDIT'):
        content = md['provenance/MILESTONE_05_' + name + '.md']
        actual = re.findall(r'^\| (M05-\d\d) \|', content, re.M)
        assert set(actual) == expected and len(actual) == len(expected), name
    git('diff', '--check')
    if args.staged:
        git('diff', '--cached', '--check')
        changed = set(git('diff', '--cached', '--name-only', BASE).decode().splitlines())
        assert changed == EDITED | ADDED, 'Index differs from verified M05 scope'
    print(json.dumps({
        'mode': 'staged' if args.staged else 'working', 'result': 'PASS',
        'baseline_files_retained':len(before), 'protected_unchanged_files':len(before)-len(EDITED),
        'scoped_existing_files':len(EDITED), 'new_files':len(ADDED), 'manifest_entries':len(manifest['files']),
        'bindings':len(bindings), 'summons':len(summons), 'master_unique_ids':len(indexed), 'names':len(names),
        'markdown_files':len(md), 'local_links_and_fragments':link_count, 'decision_groups':len(expected),
        'unchanged_arc_one_sections':len(preserved_sections), 'local_byte_snapshot_checked':args.local_bytes,
    }, indent=2))


if __name__ == '__main__':
    main()
