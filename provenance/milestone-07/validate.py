"""Read-only M07 integrity checks; carries forward applicable M04-M06 invariants; run with Python 3 from any directory.

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
BASE = 'd5bfeda394b98f6717ca5b38a3e4f3b50695c93c'
ARCHIVE = 'provenance/milestone-07/'
EDITED = set([
    ".gitattributes",
    "CONSTITUTION.md",
    "README.md",
    "live-model/INDEX.md",
    "live-model/03_KIRA.md",
    "live-model/09_ARC_ONE.md",
    "live-model/12_BOOK_RED_SIX_ARCS.md",
    "live-model/16_NEXT_THREAD_HANDOFF.md",
    "live-model/21_M04_BOOK_RED_EXPANSION.md",
    "live-model/22_CIVILIZATION_AND_WILDS.md"
])
ADDED = set([
    "provenance/MILESTONE_07_DECISION_LEDGER.md",
    "provenance/MILESTONE_07_REVERSE_SEMANTIC_AUDIT.md",
    "provenance/milestone-07/EXECUTABLE.md",
    "provenance/milestone-07/decisions/M07_BOOK_CONTINUITY.md",
    "provenance/milestone-07/SHA256_MANIFEST.json",
    "provenance/milestone-07/PRESERVATION_BASELINE.json",
    "provenance/milestone-07/validate.py",
    "references/m07-architecture/README.md",
    "references/m07-architecture/SOURCE_README.md",
    "references/m07-architecture/reference_city_01.jpeg",
    "references/m07-architecture/reference_city_02.jpeg",
    "references/m07-architecture/reference_city_03.png",
    "references/m07-architecture/reference_city_04.jpeg",
    "references/m07-architecture/reference_city_05.jpeg",
    "references/m07-architecture/reference_pedestrian_plaza.png"
])
# Previous M06 normalization is checked, not performed again.
SPELLING = {'live-model/06_STORY_AND_SAGA.md', 'live-model/09_ARC_ONE.md',
            'live-model/21_M04_BOOK_RED_EXPANSION.md'}


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
    assert set(before) == oldfiles and len(oldfiles) == 104
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
            assert expected_old.strip() in normalized(current).decode('utf-8'), f'Prior body changed: {path}'
            assert candidate != old and (b'Milestone 07' in current or b'M07' in current), path
        else:
            assert candidate == old, f'Protected content changed: {path}'
            if args.local_bytes:
                assert sha(current) == entry['sha256'] and len(current) == entry['bytes'], f'Protected bytes changed: {path}'

    manifest_bytes = read(ARCHIVE + 'SHA256_MANIFEST.json')
    assert sha(manifest_bytes) == '99f02380f438d24e6ebbe2b2566525949545f2a55af16e9c14214badcc33ae13', 'Original manifest changed'
    manifest = json.loads(manifest_bytes)
    assert len(manifest) == 9
    image_hashes = []
    baseline_image_hashes = {row['sha256'] for p,row in before.items()
                            if Path(p).suffix.lower() in {'.png','.jpeg','.jpg','.gif','.webp'}}
    for source, entry in manifest.items():
        if source == 'executable.md':
            dest = ARCHIVE + 'EXECUTABLE.md'
        elif source.startswith('references/architecture/'):
            dest = source.replace('references/architecture/', 'references/m07-architecture/', 1)
        else:
            dest = ARCHIVE + source
        payload = read(dest)
        assert len(payload) == entry['bytes'] and sha(payload) == entry['sha256'], f'Payload mismatch: {dest}'
        if dest.endswith(('.png','.jpeg')):
            assert sha(payload) not in baseline_image_hashes, f'Duplicate old image: {dest}'
            image_hashes.append(sha(payload))
            if dest.endswith('.jpeg'):
                assert payload.startswith(b'\xff\xd8') and payload.endswith(b'\xff\xd9')
            else:
                assert payload.startswith(b'\x89PNG\r\n\x1a\n')
    assert len(image_hashes) == len(set(image_hashes)) == 6
    original_text = [ARCHIVE + 'EXECUTABLE.md', ARCHIVE + 'SHA256_MANIFEST.json',
                     ARCHIVE + 'decisions/M07_BOOK_CONTINUITY.md',
                     'references/m07-architecture/SOURCE_README.md']
    attr_args = ['check-attr'] + (['--cached'] if args.staged else [])
    attrs = git(*attr_args, '-z', 'text', '--', *original_text).decode().strip('\0').split('\0')
    assert list(zip(attrs[::3], attrs[1::3], attrs[2::3])) == [
        (p, 'text', 'unset') for p in original_text], 'Original payload checkout conversion enabled'
    if args.staged:
        for path in original_text:
            assert git('cat-file', '--filters', '--path=' + path, ':' + path) == read(path), path
    assert {p for p in ADDED if p.endswith(('.png','.jpeg','.jpg'))} == {
        p for p in files-oldfiles if p.endswith(('.png','.jpeg','.jpg'))}
    assert not any(p.startswith(('live-model/14_', 'live-model/24_', 'references/m06-cartography/'))
                   for p in EDITED | ADDED), 'M07 must not change cartographic workflow/assets'

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
    workshop = md['provenance/milestone-06/decisions/M06_WORKSHOP.md']
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
    # M07 review coverage is separate from the unchanged M06 table above.
    expected = {f'M07-{i:02d}' for i in range(1,31)}
    for name in ('DECISION_LEDGER','REVERSE_SEMANTIC_AUDIT'):
        content = md['provenance/MILESTONE_07_' + name + '.md']
        actual = re.findall(r'^\| (M07-\d\d) \|', content, re.M)
        assert set(actual) == expected and len(actual) == len(expected), name
        assert all(f'[§{i}]' in content for i in range(1,5)), 'Missing M07 source section'
    ledger = md['provenance/MILESTONE_07_DECISION_LEDGER.md']
    classifications = re.findall(r'^\| M07-\d\d \| [^|]+ \| (PRESENT|PARTIAL|MISSING|CONFLICT) \|', ledger, re.M)
    assert Counter(classifications) == {'PRESENT':9,'PARTIAL':11,'MISSING':9,'CONFLICT':1}
    decisions = md[ARCHIVE + 'decisions/M07_BOOK_CONTINUITY.md']
    assert len(re.findall(r'^## ',decisions,re.M)) == 4
    opening = section(live('21_M04_BOOK_RED_EXPANSION'), 'Milestone 07 Arc II apartment opening')
    assert all(t in opening for t in (
        'in medias res', 'first apartment', 'city gates', 'no', 'ILLUSTRATIVE',
        '500 versus comparable 370', 'currency', 'surcharge', 'market rule',
        'signing outcome', 'landlord identity', 'dialogue', 'OPEN',
        'socially sideways, not upward', 'perceived as Afflicted',
        'noncontagious genetic condition', 'not all individuals behave alike',
        'prepared chainmail rings', 'proposed three-basin', 'novice card control',
        'neither instant business success nor bargaining mastery'))
    biography = section(live('03_KIRA'), 'Milestone 07 restoration and social standing')
    assert all(t in biography for t in ('healthy white skin','class hierarchy','perceived as Afflicted','beneath','housing, employment, pricing and social opportunities'))
    city = section(civic, 'Milestone 07 Afflicted social continuity')
    assert all(t in city for t in ('Eternal Ladder gestures and direct harassment','Individuals vary','noncontagious genetic condition','noble/commoner/peasant','Afflicted commoner'))
    architecture = section(civic, 'Milestone 07 ordinary city architecture')
    assert all(t in architecture for t in ('limestone','marble','sandstone','ivory','L-shaped','flat roofs','2–4 occupied stories','terraces','arcades','planted courtyards','open plazas','fountains','where mapped','Blackstone','functional identifiers, not roof colors','symmetrical palace layouts','relocated roads','Procreate-layer','author will provide maps'))
    handoff = live('16_NEXT_THREAD_HANDOFF')
    assert handoff.startswith('# Current next-thread starting position — M07, Book Red Arc II')
    assert 'SUPERSEDED as workshop starting positions only' in handoff
    current_handoff = section(handoff,'Milestone 07 current handoff — Arc II')
    assert all(t in current_handoff for t in ('haggling over her first apartment','not written prose','25_CONTINENTAL','26_CHAPTER','MILESTONE_06_DECISION','MILESTONE_06_SOURCE','MILESTONE_06_REVERSE','exact city identity'))
    assert 'Current starting point — M07' in live('INDEX')
    # Inspect only new prose for current spelling; earlier historical usages are immutable.
    for path in EDITED:
        content = normalized(read(path)).decode('utf-8')
        old = git('show', BASE + ':' + path).decode('utf-8').strip()
        addition = content.replace(old,'',1)
        assert not re.search(r'\babeca\b|\bAbecca\b',addition), f'M07 beverage spelling: {path}'
        for line in addition.splitlines():
            if re.search(r'\bKira\b',line):
                assert 'shorthand' in line, f'M07 manuscript/shorthand distinction: {path}'
    for m,count in [('04',43),('05',35),('06',42)]:
        for name in ('DECISION_LEDGER','REVERSE_SEMANTIC_AUDIT'):
            ids = re.findall(r'^\| M' + m + r'-(\d\d) \|',md['provenance/MILESTONE_'+m+'_'+name+'.md'],re.M)
            assert len(ids) == count and len(set(ids)) == count, f'Prior coverage lost: M{m}'
    git('diff', '--check')
    if args.staged:
        git('diff', '--cached', '--check')
        changed = set(git('diff', '--cached', '--name-only', BASE).decode().splitlines())
        assert changed == EDITED | ADDED, 'Index differs from verified M07 scope'
    print(json.dumps({
        'mode': 'staged' if args.staged else 'working', 'result': 'PASS',
        'baseline_files_retained':len(before), 'protected_unchanged_files':len(before)-len(EDITED),
        'scoped_existing_files':len(EDITED), 'new_files':len(ADDED), 'manifest_entries':len(manifest),
        'bindings':len(bindings), 'summons':len(summons), 'master_unique_ids':len(indexed), 'names':len(names),
        'markdown_files':len(md), 'local_links_and_fragments':link_count, 'decision_groups':len(expected), 'source_sections':4, 'archived_images':6, 'proposed_names_verified':4,
        'arc_one_sections_preserved':len(preserved_sections), 'local_byte_snapshot_checked':args.local_bytes,
    }, indent=2))


if __name__ == '__main__':
    main()
