import unittest

from insurance.eligibility import EligibilityError, parse_eligibility_response

PAYER = {"id": "84980", "name": "Blue Cross Blue Shield of Texas"}


def _cov(status="active", group="G1", maternity=True):
    return {
        "status": status,
        "planName": "BCBSTX PPO",
        "groupNumber": group,
        "benefits": [{"serviceType": "maternity", "covered": maternity}],
    }


class ParseEligibilityTest(unittest.TestCase):
    def test_coverages_list_api_2026_10_01(self):
        # Regression for ERR-F1B5091122: KeyError 'coverage' on the new coverages list.
        result = parse_eligibility_response(
            {"status": "complete", "payer": PAYER, "coverages": [_cov(group=None)]}
        )
        self.assertTrue(result.eligible)
        self.assertTrue(result.maternity_covered)
        self.assertEqual(result.group_number, "")

    def test_prefers_active_coverage(self):
        result = parse_eligibility_response(
            {"status": "complete", "payer": PAYER,
             "coverages": [_cov(status="inactive"), _cov(group=" G2 ")]}
        )
        self.assertTrue(result.eligible)
        self.assertEqual(result.group_number, "G2")

    def test_legacy_single_coverage(self):
        result = parse_eligibility_response({"status": "complete", "payer": PAYER, "coverage": _cov()})
        self.assertTrue(result.eligible)
        self.assertEqual(result.group_number, "G1")

    def test_empty_coverages_raises_eligibility_error(self):
        with self.assertRaises(EligibilityError):
            parse_eligibility_response({"status": "complete", "payer": PAYER, "coverages": []})


if __name__ == "__main__":
    unittest.main()
