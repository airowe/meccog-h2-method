import os, sys, unittest

sys.path.insert(0, os.path.dirname(__file__))
from compare_audit import parse_eff, eff_agree, norm_p, norm_n, compare


class ParseEffTest(unittest.TestCase):
    def test_percent_forms_give_magnitude(self):
        for text, want in [('~60%', 60.0), ('-38%', 38.0), ('about 45% lower', 45.0),
                           ('~+56% (~0.98 vs ~1.53)', 56.0)]:
            self.assertEqual(parse_eff(text), want, text)

    def test_fold_becomes_percent_change(self):
        self.assertAlmostEqual(parse_eff('1.5x'), 50.0)
        self.assertAlmostEqual(parse_eff('~2-fold'), 100.0)

    def test_non_numeric(self):
        for text in ['N/A', 'qualitative', '', None]:
            self.assertIsNone(parse_eff(text), text)


class EffAgreeTest(unittest.TestCase):
    def test_within_tolerance_ignoring_sign(self):
        self.assertTrue(eff_agree('~60%', '-55%'))

    def test_outside_tolerance(self):
        self.assertFalse(eff_agree('~60%', '~20%'))

    def test_both_non_numeric_agree(self):
        self.assertTrue(eff_agree('N/A', 'qualitative'))

    def test_one_numeric_one_missing_disagree(self):
        self.assertFalse(eff_agree('~60%', 'N/A'))


class NormPTest(unittest.TestCase):
    def test_spacing_and_case(self):
        self.assertEqual(norm_p('P < 0.05'), '<0.05')
        self.assertEqual(norm_p('n/a'), 'N/A')


class NormNTest(unittest.TestCase):
    def test_leading_count_ignores_unit_words(self):
        self.assertEqual(norm_n('3 biological replicates per genotype'), norm_n('3'))
        self.assertEqual(norm_n('65-86 cells from 6-8 preparations'), norm_n('65-86'))

    def test_different_counts_differ(self):
        self.assertNotEqual(norm_n('3 replicates'), norm_n('4'))
        self.assertNotEqual(norm_n('N/A'), norm_n('3'))


class CompareTest(unittest.TestCase):
    OURS = {'eff': '~60%', 'eff_prov': 'estimated_from_figure', 'p': '<0.001',
            'p_prov': 'visual_only', 'n': '3', 'n_prov': 'printed_in_text',
            'against': False, 'class': 3}

    def test_identical_has_no_diffs(self):
        self.assertEqual(compare(self.OURS, dict(self.OURS)), [])

    def test_reports_each_field_that_differs(self):
        blind = dict(self.OURS, p='<0.01', against=True, eff='~20%')
        self.assertEqual(sorted(compare(self.OURS, blind)), ['against', 'eff', 'p'])


if __name__ == '__main__':
    unittest.main()
