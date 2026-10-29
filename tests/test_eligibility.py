import unittest

from insurance.eligibility import EligibilityError, parse_eligibility_response


PAYER = {"id": "60054", "name": "Aetna"}


def _cov(status="active", group="G1 ", maternity=True):
    return {"status": status, "planName": "Aetna PPO", "groupNumber": group,
            "benefits": [{"serviceType": "maternity", "covered": maternity}]}


class ParseEligibilityTest(unittest.TestCase):
    def test_coverages_list_api_2026_10_01(self):
        r = parse_eligibility_response({"payer": PAYER, "coverages": [_cov(group=None)]})
        self.assertTrue(r.eligible)
        self.assertEqual(r.plan_name, "Aetna PPO")
        self.assertEqual(r.group_number, "")
        self.assertTrue(r.maternity_covered)

    def test_prefers_active_coverage(self):
        r = parse_eligibility_response({"payer": PAYER, "coverages": [_cov("inactive"), _cov("active", "G2")]})
        self.assertTrue(r.eligible)
        self.assertEqual(r.group_number, "G2")

    def test_legacy_single_coverage(self):
        r = parse_eligibility_response({"payer": PAYER, "coverage": _cov()})
        self.assertTrue(r.eligible)
        self.assertEqual(r.group_number, "G1")

    def test_no_coverage_raises_eligibility_error(self):
        with self.assertRaises(EligibilityError):
            parse_eligibility_response({"payer": PAYER, "coverages": []})


if __name__ == "__main__":
    unittest.main()
