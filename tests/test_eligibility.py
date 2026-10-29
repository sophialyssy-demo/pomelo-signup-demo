import unittest

from insurance.eligibility import EligibilityError, parse_eligibility_response

PAYER = {"id": "84980", "name": "Blue Cross Blue Shield of Texas"}


def _coverage(status="active", group="GRP1"):
    return {
        "status": status,
        "planName": "BCBSTX PPO",
        "groupNumber": group,
        "benefits": [{"serviceType": "maternity", "covered": True}],
    }


class ParseEligibilityTest(unittest.TestCase):
    def test_coverages_list_api_2026_10_01(self):
        # Regression for ERR-CF9A817FC4: KeyError 'coverage' on the new coverages list shape.
        result = parse_eligibility_response({
            "status": "complete", "payer": PAYER,
            "coverages": [_coverage(status="inactive"), _coverage(group=None)],
        })
        self.assertTrue(result.eligible)
        self.assertEqual(result.group_number, "")
        self.assertTrue(result.maternity_covered)

    def test_legacy_single_coverage(self):
        result = parse_eligibility_response({"status": "complete", "payer": PAYER, "coverage": _coverage(group=" G1 ")})
        self.assertTrue(result.eligible)
        self.assertEqual(result.group_number, "G1")

    def test_empty_coverages_raises_eligibility_error(self):
        with self.assertRaises(EligibilityError):
            parse_eligibility_response({"status": "complete", "payer": PAYER, "coverages": []})


if __name__ == "__main__":
    unittest.main()
