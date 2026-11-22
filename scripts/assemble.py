"""Build H2_submission.xlsx from the official template and rows/<PMID>.json.

The template is copied, never edited in place. Paper order is ORDER below
(most relevant first); findings keep the order of each JSON file.
"""
import json, os, shutil, sys
import openpyxl

BASE = os.path.expanduser('~/Documents/Alzheimers')
WORK = os.path.join(BASE, 'H2_work')
TEMPLATE = os.path.join(BASE, 'submission_template.xlsx')
OUT = os.path.join(BASE, 'H2_submission.xlsx')

HYPOTHESIS = ("In some types of non-Alzheimer's, non-aged human brain cells, for example astrocytes, "
              "APOE4 causes impaired ARF6-related recycling of receptors between the cell surface and "
              "the endosome, compared with APOE3.")
# Keys are rows/<key>.json names: the PMID, or a slug for a source with no PMID.
ORDER = ['31641056', '30375977', '38217595', '20547867', '29946028', '28957663', '31796678',
         '39532095', '34617884', '39901180', '24251389', '33027662', '42239208', '32588544',
         '29861287', '40845853', '43026723', '35031484', '41292981', '10880397', '12507910', '29311783',
         '40675218', '34557909', 'ralhan2026', '37777962', 'kerman2023', '35969759']
STRENGTH = {1: '1 very strong', 2: '2 strong', 3: '3 moderate', 4: '4 weak', 5: '5 very weak'}
# Method-sheet values live in an untracked local file (contains contact details).
METHOD = json.load(open(os.path.join(WORK, 'method.local.json')))


def main(order=ORDER):
    shutil.copyfile(TEMPLATE, OUT)
    wb = openpyxl.load_workbook(OUT)
    ws = wb['Submission']
    ws['A2'] = HYPOTHESIS
    r = 3
    counts = {'papers': 0, 'findings': 0, 'against': 0}
    for pi, key in enumerate(order, 1):
        rows = json.load(open(os.path.join(WORK, 'rows', f'{key}.json')))
        paper, findings = rows[0], [x for x in rows[1:] if not x.get('paper')]
        assert paper.get('paper') and str(paper.get('key', paper['pmid'])) == key, key
        ws.cell(r, 2, paper['doi']); ws.cell(r, 3, paper['source_type'])
        ws.cell(r, 4, str(paper['pmid'])); ws.cell(r, 5, f'P{pi}')
        r += 1
        counts['papers'] += 1
        for fi, f in enumerate(findings, 1):
            vals = [f'P{pi}.F{fi}', f['description'], f['quote'], f['summary'], str(f['relevance']),
                    f['system'], f['location'], f['eff'], f['eff_prov'], f['p'], f['p_prov'],
                    f['n'], f['n_prov'], str(f['class']), STRENGTH[f['strength']]]
            for ci, v in enumerate(vals, 5):
                ws.cell(r, ci, v)
            r += 1
            counts['findings'] += 1
            counts['against'] += bool(f.get('against'))
    m = wb['Method']
    for row in range(1, 8):
        label = m.cell(row, 1).value
        m.cell(row, 2, METHOD[label])
    wb.save(OUT)
    print(OUT, counts)


if __name__ == '__main__':
    main(sys.argv[1:] or ORDER)
