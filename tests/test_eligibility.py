import unittest

from insurance.eligibility import EligibilityError, parse_eligibility_response


def _coverage(status="active", group=" G1 ", maternity=True):
    return {
        "status": status,
        "planName": "Aetna PPO",
        "groupNumber": group,
        "benefits": [{"serviceType": "maternity", "covered": maternity}],
    }


class ParseEligibilityResponseTest(unittest.TestCase):
    def test_coverages_list(self):
        # Regression for ERR-EBF01F24DE: API 2026-10-01 returns a `coverages` list.
        result = parse_eligibility_response({
            "payer": {"name": "Aetna"},
            "coverages": [_coverage(status="inactive", group=None), _coverage()],
        })
        self.assertTrue(result.eligible)
        self.assertEqual(result.group_number, "G1")
        self.assertTrue(result.maternity_covered)

    def test_null_group_number(self):
        result = parse_eligibility_response({"payer": {"name": "Aetna"}, "coverages": [_coverage(group=None)]})
        self.assertEqual(result.group_number, "")

    def test_legacy_coverage_object(self):
        result = parse_eligibility_response({"payer": {"name": "Aetna"}, "coverage": _coverage()})
        self.assertTrue(result.eligible)

    def test_no_coverage(self):
        with self.assertRaises(EligibilityError):
            parse_eligibility_response({"payer": {"name": "Aetna"}, "coverages": []})


if __name__ == "__main__":
    unittest.main()
