"""Compare blind audit rows with our coded rows and list field disagreements.

Usage: compare_audit.py <blind.json>...   (writes nothing; prints a report)
Effect sizes are compared as magnitudes of percent change: a sign or wording
difference ("lower" vs a negative number) is not a disagreement, a size is.
"""
import json, os, re, sys

WORK = os.path.expanduser('~/Documents/Alzheimers/H2_work')
ABS_TOL_PP = 15.0
REL_TOL = 0.25
FIELDS = ['eff_prov', 'p', 'p_prov', 'n', 'n_prov', 'against', 'class']

PERCENT = re.compile(r'([-+]?\d+(?:\.\d+)?)\s*%')
FOLD = re.compile(r'(\d+(?:\.\d+)?)\s*(?:x|-?fold)\b', re.I)


def parse_eff(text):
    if not text:
        return None
    m = PERCENT.search(text)
    if m:
        return abs(float(m.group(1)))
    m = FOLD.search(text)
    if m:
        return abs(float(m.group(1)) - 1) * 100
    return None


def eff_agree(ours, blind):
    a, b = parse_eff(ours), parse_eff(blind)
    if a is None or b is None:
        return a is None and b is None
    return abs(a - b) <= max(ABS_TOL_PP, REL_TOL * max(a, b))


def norm_p(text):
    t = re.sub(r'\s+', '', str(text or '')).lower().lstrip('p')
    return 'N/A' if t in ('n/a', 'na', '') else t


LEADING_COUNT = re.compile(r'^~?\s*(\d+(?:\s*[-–]\s*\d+)?)')


def norm_n(text):
    t = str(text or '').strip()
    m = LEADING_COUNT.match(t)
    if m:
        return re.sub(r'\s|–', lambda x: '-' if x.group() == '–' else '', m.group(1))
    return re.sub(r'\s+', '', t).lower()


def compare(ours, blind):
    diffs = [] if eff_agree(ours.get('eff'), blind.get('eff')) else ['eff']
    for f in FIELDS:
        a, b = ours.get(f), blind.get(f)
        if f == 'p':
            a, b = norm_p(a), norm_p(b)
        elif f == 'n':
            a, b = norm_n(a), norm_n(b)
        elif f == 'class':
            a, b = int(a) if a is not None else None, int(b) if b is not None else None
        elif f == 'against':
            a, b = bool(a), bool(b)
        if a != b:
            diffs.append(f)
    return diffs


def ours_by_id():
    out = {}
    for name in os.listdir(os.path.join(WORK, 'rows')):
        rows = json.load(open(os.path.join(WORK, 'rows', name)))
        key = name[:-5]
        for i, f in enumerate([x for x in rows[1:] if not x.get('paper')], 1):
            out[f'{key}#{i}'] = f
    return out


def main(paths):
    ours = ours_by_id()
    total = clean = 0
    for path in paths:
        for b in json.load(open(path)):
            total += 1
            o = ours[b['id']]
            diffs = compare(o, b)
            if not diffs:
                clean += 1
                continue
            print(f"\n== {b['id']}  [{', '.join(diffs)}]  blind dir={b.get('direction')}")
            for f in ['eff'] + FIELDS:
                if f in diffs:
                    print(f'   {f:9} ours={o.get(f)!s:40.40} blind={b.get(f)!s:.60}')
            if b.get('notes'):
                print(f"   notes: {b['notes'][:300]}")
    print(f'\n{clean}/{total} items agree on every compared field')


if __name__ == '__main__':
    main(sys.argv[1:])
