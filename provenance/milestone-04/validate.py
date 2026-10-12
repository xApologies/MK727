"""Read-only M04 integrity checks; run from any working directory with Python 3.

--staged validates the complete index instead of working files.
--local-bytes additionally verifies the original Windows working-byte snapshot.
The human reverse semantic audit is separate from these mechanical checks.
"""
from pathlib import Path
from urllib.parse import unquote, urlsplit
from collections import Counter
import argparse
import csv
import hashlib
import io
import json
import re
import subprocess
import unicodedata

ROOT = Path(__file__).resolve().parents[2]
BASE = '7c5c32fd875f0b9fcd35aba39824cc9c1faf2c66'
ARCHIVE = 'provenance/milestone-04/'
EDITED = {
    'README.md', 'CONSTITUTION.md', 'INHERITANCE.md', 'live-model/INDEX.md',
    *('live-model/' + name for name in (
        '02_WORLD.md', '03_KIRA.md', '06_STORY_AND_SAGA.md', '07_BLACK_CARDS.md',
        '08_EDUCATION_PROFESSIONS.md', '09_ARC_ONE.md', '11_DECISION_LEDGER.md',
        '12_BOOK_RED_SIX_ARCS.md', '13_DIMENSIONAL_RING_AND_TOURNAMENT.md',
        '16_NEXT_THREAD_HANDOFF.md')),
}
NEW_DOCS = {'live-model/' + name for name in (
    '17_MATERIAL_MANIPULATION.md', '18_CARDSMITHING_WORKSPACE.md',
    '19_ANTAGONISTS.md', '20_REALMS_AND_STARSCAPE.md', '21_M04_BOOK_RED_EXPANSION.md')}


def git(*args):
    return subprocess.check_output(['git', *args], cwd=ROOT)


def sha(data):
    return hashlib.sha256(data).hexdigest()


def normalized(data):
    return data.replace(b'\r\n', b'\n')


def anchors(text):
    counts = Counter()
    values = set()
    for heading in re.findall(r'^#{1,6}\s+(.+?)\s*#*$', text, re.M):
        heading = re.sub(r'\[([^]]+)\]\([^)]*\)', r'\1', heading)
        heading = re.sub(r'<[^>]+>|[`*_~]', '', heading).lower()
        slug = ''.join(c for c in heading if not unicodedata.category(c).startswith('P') or c in '-_')
        slug = slug.replace(' ', '-')
        n = counts[slug]
        counts[slug] += 1
        values.add(slug + (f'-{n}' if n else ''))
    return values


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--staged', action='store_true')
    ap.add_argument('--local-bytes', action='store_true')
    args = ap.parse_args()
    assert not (args.staged and args.local_bytes), 'Local bytes apply only to working files'
    if args.staged:
        files = set(git('ls-files', '-z').decode().strip('\0').split('\0'))
        read = lambda path: git('show', ':' + path)
    else:
        files = set(git('ls-files', '-z', '--cached', '--others', '--exclude-standard').decode().strip('\0').split('\0'))
        read = lambda path: (ROOT / path).read_bytes()
    assert all(not ({'_inbox', '.inbox'} & set(Path(p).parts)) for p in files), 'Inbox included'
    assert not git('ls-files', '-u'), 'Unmerged index entries'
    baseline = json.loads(read(ARCHIVE + 'PRESERVATION_BASELINE.json').decode('utf-8-sig'))
    before = {row['path']: row for row in baseline}
    original_files = set(git('ls-tree', '-r', '--name-only', BASE).decode().splitlines())
    assert set(before) == original_files
    assert original_files <= files, 'Historical file removed'
    changed = []
    for path, entry in before.items():
        old = git('show', BASE + ':' + path)
        current = read(path)
        if path in EDITED:
            assert old in normalized(current), f'Original text not retained: {path}'
            assert b'Milestone 04' in current
            changed.append(path)
        else:
            # Git blob comparison preserves binary bytes and ignores only checkout CRLF for text.
            candidate = normalized(current) if b'\0' not in old and path.endswith(('.md', '.csv', '.txt', '.json')) else current
            assert candidate == old, f'Protected content changed: {path}'
        if args.local_bytes:
            if path in EDITED:
                start = current.index(b'\n\n') + 2 if current.startswith(b'> **Current M04 authority:') else 0
                assert sha(current[start:start + entry['bytes']]) == entry['sha256'], path
            else:
                assert sha(current) == entry['sha256'], f'Protected bytes changed: {path}'
    allowed_added = NEW_DOCS | {
        'provenance/MILESTONE_04_DECISION_LEDGER.md',
        'provenance/MILESTONE_04_REVERSE_SEMANTIC_AUDIT.md',
        'references/genesis-point-antagonists/README.md', 'references/m04-visuals/README.md',
        ARCHIVE + 'EXECUTABLE.md', ARCHIVE + 'SHA256_MANIFEST.json',
        ARCHIVE + 'PRESERVATION_BASELINE.json', ARCHIVE + 'SOURCE_REGISTER.json',
        ARCHIVE + 'validate.py', ARCHIVE + 'audit/BASELINE.md',
    }
    manifest = json.loads(read(ARCHIVE + 'SHA256_MANIFEST.json'))
    for path, entry in manifest.items():
        if path == 'executable.md':
            dest = ARCHIVE + 'EXECUTABLE.md'
        elif path.startswith('references/genesis-point/'):
            dest = path.replace('references/genesis-point/', 'references/genesis-point-antagonists/')
        elif path.startswith('references/visuals/'):
            dest = path.replace('references/visuals/', 'references/m04-visuals/')
        else:
            dest = ARCHIVE + path
        allowed_added.add(dest)
        data = read(dest)
        assert len(data) == entry['bytes'] and sha(data) == entry['sha256'], f'Payload mismatch: {dest}'
    assert files - original_files == allowed_added, f'Unexpected or missing additions: {(files-original_files) ^ allowed_added}'

    def rows(name):
        return list(csv.DictReader(io.StringIO(read('catalogues/genesis-cards/' + name).decode('utf-8-sig'))))

    bindings = rows('MK727_BINDINGS_FULL.csv')
    summons = rows('MK727_SUMMONS_FULL.csv')
    master = rows('MK727_GENESIS_CARD_MASTER_1245.csv')
    assert [len(bindings), len(summons), len(master)] == [1016, 229, 1245]
    assert len({r['mk727_card_id'] for r in master}) == 1245
    indexed = {r['source_id']: r for r in master}
    assert len(indexed) == 1245
    for row in bindings + summons:
        source_id = row.get('id') or row['entity_id']
        assert all(indexed[source_id].get(k) == v for k, v in row.items()), source_id
    assert len(rows('MK157_ORIGINAL_BINDINGS.csv')) == 1016
    assert len(rows('MK157_ORIGINAL_SUMMONED_ENTITIES.csv')) == 229
    dist = Counter(len(json.loads(r['required_basins'])) for r in bindings)
    assert dist == {2: 264, 3: 692, 4: 60}
    for row in bindings + summons:
        basins = json.loads(row['required_basins'])
        assert len(basins) == len(set(basins)) and set(basins) <= {'Red','Orange','Yellow','Green','Blue','Violet'}
    ids = {r['id']: r for r in bindings}
    assert ids['GF-0011']['name'] == 'Expanded Genesis Sight'
    assert ids['GF-0019']['name'] == 'Expanded Transduction Trace'
    assert json.loads(ids['GF-0011']['required_basins']) == ['Orange','Green','Blue']
    assert json.loads(ids['GF-0019']['required_basins']) == ['Red','Yellow','Green']
    name_rows = list(csv.DictReader(io.StringIO(read('catalogues/names/names.csv').decode('utf-8-sig'))))
    assert len(name_rows) == 185

    md = {p: read(p).decode('utf-8') for p in files if p.endswith('.md')}
    link_count = 0
    for path, content in md.items():
        assert '\ufffd' not in content and not any(ord(c) < 32 and c not in '\r\n\t' for c in content), path
        # Inline Markdown links; all repository links use this form.
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
    ledger = md['provenance/MILESTONE_04_DECISION_LEDGER.md']
    audit = md['provenance/MILESTONE_04_REVERSE_SEMANTIC_AUDIT.md']
    expected_ids = {f'M04-{i:02d}' for i in range(1,44)}
    assert set(re.findall(r'M04-\d\d', ledger)) == expected_ids
    assert set(re.findall(r'M04-\d\d', audit)) == expected_ids
    git('diff', '--check')
    if args.staged:
        git('diff', '--cached', '--check')
        staged = set(git('diff', '--cached', '--name-only', BASE).decode().splitlines())
        assert staged == EDITED | allowed_added, 'Index differs from M04 scope'
    print(json.dumps({
        'mode': 'staged' if args.staged else 'working', 'result': 'PASS',
        'baseline_files_retained': len(before), 'unchanged_files': len(before)-len(EDITED),
        'original_text_preserved_in_modified_files': len(EDITED), 'new_files': len(allowed_added),
        'manifest_entries': len(manifest), 'bindings': len(bindings), 'summons': len(summons),
        'master_unique_ids': len(indexed), 'names': len(name_rows),
        'markdown_files': len(md), 'local_links_and_fragments': link_count,
        'decision_groups': len(expected_ids), 'local_byte_snapshot_checked': args.local_bytes,
    }, indent=2))


if __name__ == '__main__':
    main()
