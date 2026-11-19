# Method

MecCog Step 1 submission.

- **Team:** Groovy
- **Hypothesis:** H2, impaired ARF6-related receptor recycling. "In some types of non-Alzheimer's, non-aged human brain cells, for example astrocytes, APOE4 causes impaired ARF6-related recycling of receptors between the cell surface and the endosome, compared with APOE3."
- **Submission date:** FILL IN ON SUBMISSION

---

## 1. Who did the work

A person and an agent (`both`). One human team leader set the task, the scope and the rules, and reviewed the output. One orchestrating agent did the searching, ranking, full-text retrieval and review, and assembled the sheet. It handed per-paper extraction to five sub-agents running the same model. Each sub-agent got one or two papers and the same written brief (`prompts/EXTRACTION_BRIEF.md`). The orchestrator then checked every sub-agent's rows (section 5) and corrected them before assembly. The human's checks are listed in section 5.

## 2. Model and version

- Orchestrator: `claude-opus-5-5` (Anthropic), run in Claude Code (desktop app).
- Extraction sub-agents (5): `claude-opus-5-5`, run in the same Claude Code session.

## 3. How papers were found

The searches ran on 2026-11-19.

- **PubMed (NCBI E-utilities):** 18 boolean queries combining `APOE4 OR apoE4` with each of the following:
  - recycling; ARF6; ABCA1 trafficking
  - NHE6/SLC9A6; Rab11/Rab4/recycling endosome
  - LRP1/LDLR/ApoER2/LRP8/SORLA with surface/recycling/internalization
  - insulin receptor; endocytosis/early endosome with astrocyte/iPSC
  - glutamate receptor surface; transferrin receptor; endosome with iPSC
  - sortilin/SORLA/retromer; LRP1 with astrocyte; cell-surface receptor
  - endolysosomal trafficking; Reelin/ApoER2/VLDLR; TREM2/GLUT/EGFR surface

  The exact strings are in `scripts/pm.py` usage and the session log.
- **Forward citations:** the Europe PMC citations API, for 7 key papers. Results were title-filtered for APOE plus a trafficking term.
- **Screening:** about 120 unique records were screened on title, and 25 on abstract. 12 were kept.
- **Searches that added nothing usable:**
  - `APOE4 AND ARF6` returned only the starting reference.
  - `APOE4 AND Rab11/Rab4` returned 1 record (the same paper).
  - Sortilin/SORL1 queries returned genetics-association papers, none measuring recycling.
  - TREM2/GLUT/EGFR queries found no APOE-isoform receptor-surface papers.
- **Ranking:** papers were ordered by how directly they measure receptor surface level or recycling under APOE4 vs APOE3, then by closeness of the system to human brain cells.

## 4. How full text was obtained

Routes were tried in this order:

1. Europe PMC `fullTextXML`
2. NCBI PMC efetch
3. NCBI BioC
4. the PMC article HTML page
5. Unpaywall, then the publisher
6. the human's own Chrome browser, for pages that block scripts

Figure images came from PMC, the eLife CDN or the Springer CDN, and were inspected visually to read significance marks and panel content. Supplements were requested through Europe PMC `supplementaryFiles`.

**Main text:** 11 of 12 papers were obtained in full.

- Narayan 2020 came through Chrome (PMC author manuscript).
- Cheng 2026 (Glycobiology) is an open-access accepted manuscript, published only as a PDF. It was read in Chrome; its abstract, the relevant Results paragraph, the cell-source sentence and the Fig 4 legend were transcribed for quote checking.
- Feng 2020 (J Alzheimers Dis) is subscription-only and is recorded from its abstract with `full_text_unavailable`.

**Supplements:** Lee 2025 came through Europe PMC. Scripted requests for the other three were blocked by bot checks, so the Prasad 2018 SI Appendix, the Zhao 2017 NIHMS supplement and the Narayan 2020 supplement were read as PDFs in Chrome, from PMC. The figure legends quoted from the Prasad SI were transcribed into the full-text file for quote checking. All supplement statistics are now read: only the 2 Feng 2020 abstract rows carry `full_text_unavailable`.

## 5. What a human checked

**Automated and agent checks, on 100% of rows:**

- **DOI/PMID:** every DOI matches the DOI PubMed lists for its PMID. A deliberately wrong pair was caught as a negative control.
- **Quote:** every quote is a verbatim substring of the retrieved full text (`scripts/check_rows.py`, with a self-test that catches 6/6 seeded defects).
- **Statistic fields:** shape and provenance pairing is valid.
- **Estimates:** `~` appears only with `estimated_from_figure`, and no P value is estimated.
- **Quote position:** the cited figure is mentioned within 600 characters of the quote (`scripts/quote_near_fig.py`, with a positive and a negative control). Every shortlisted row was read by the orchestrator. In the final run, 7 of 72 were shortlisted, and all are legend or Results sentences sitting under the right figure. In an earlier run, 1 quote was replaced.
- **Official validator** (`validate_submission.py` from the challenge page): no errors in the Submission sheet.

**Orchestrator review of every sub-agent row:**

- **P values:** exact values printed on a figure panel were recoded to `printed_in_text`.
- **Wrong comparison:** where significance brackets compared ApoE4 with a no-ApoE control rather than with ApoE3, the row now says so. A P value attached to a contrast the row does not describe was set to N/A.
- **Off-topic rows:** three were removed.
- **Figures:** four Zhao 2017 figures were read in the browser to replace codes the sub-agent assigned because it had not seen the images.

**Human (team leader):** FILL IN. State the number of rows checked against the source PDF, and what was checked: quote, panel, statistics and directness. The recommendation is all rows with `estimated_from_figure` (42) or `full_text_unavailable` (2), plus a random 10 of the rest.

## 6. Anything else

- **Hypothesis boundary.**
  - "Receptor recycling" was read as: the surface level, endosomal retention or recycling rate of a cell-surface receptor or transporter (ABCA1, LRP1, ApoER2, NMDA/AMPA receptors, insulin receptor, transferrin receptor).
  - Ligand-uptake and endosome-marker readouts are included as class 3 surrogates.
  - Endosomal pH (NHE6) is included only as the proposed cause of the recycling block.
  - Only Rawat 2019 links ARF6 itself to APOE4. Its ARF6 evidence is a change in total ARF6 protein and an ARF6-knockdown efflux readout; no ARF6-dependent recycling assay was found anywhere.
- **Against or null findings:** 15 of 72. The strongest is a direct pulse-chase in isogenic human iPSC brain endothelial cells (Bell 2025, Fig 6D), which shows an unchanged transferrin recycling rate. Others:
  - unchanged surface Lrp1, Ldlr, insulin receptor and transferrin receptor in ApoE4-treated rat neurons (Xian 2018, Fig 2C);
  - unchanged Rab11 recycling endosomes in iPSC astrocytes (Narayan 2020);
  - unchanged ABCA1 in non-aged mice and in human cortex (Lee 2025).
- **Effect sizes:**
  - Most figures print no percentage. Values read off bars carry `~` and `estimated_from_figure`.
  - Where the authors printed "~N%", it is recorded as printed, without the tilde, because the format reserves `~` for figure estimates.
  - A percentage-point difference in colocalization is recorded as the authors define it.
- **Model systems:** most evidence comes from mouse or rat neurons and astrocytes treated with exogenous ApoE, from ApoE-targeted-replacement mice, or from isogenic human iPSC cells. Each row names its deviation from the hypothesis's "non-aged, non-AD human brain cell". Lee 2025 rows from 18- and 22-month mice are flagged as aged.
- **Statistic belongs to the contrast:** where a printed P value compares something other than APOE4 vs APOE3, it is not used. One example is Cheng 2026 Fig 4: p = 0.004 compares Rab5 with Rab7 within APOE4/4 cells. Such rows carry `N/A` with `not_found_in_source`, and the human_check note says why.
- **Shared donor:** Coriell AG10788 (87 years, late-onset AD, APOE4/4) is the APOE4 parental line in Narayan 2020 and the APOE4/4 fibroblast line in Cheng 2026. The two papers are not independent on the APOE4 side.
- **Not included:** papers on apoE particle recycling itself (not receptor recycling) were excluded, as were reviews.

## Code and prompts

- `scripts/pm.py`: PubMed search and summary.
- `scripts/citers.py`: forward citations.
- `scripts/totext.py`: JATS/HTML to text.
- `scripts/check_rows.py`: row checker, with `--selftest`.
- `scripts/quote_near_fig.py`: quote-to-panel proximity shortlist.
- `scripts/assemble.py`: builds the spreadsheet from `rows/*.json` and the official template. Method-sheet contact details live in an untracked local file.
- `prompts/EXTRACTION_BRIEF.md`: the exact brief given to the extraction sub-agents.
- `rows/<PMID>.json`: the per-paper findings that make up the submission.

Full texts are not redistributed. Code is under the MIT license.
