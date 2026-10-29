import unittest

from insurance.eligibility import EligibilityError, parse_eligibility_response, verify_eligibility

PAYER = {"id": "60054", "name": "Aetna"}
COV = {"status": "active", "planName": "Aetna PPO", "groupNumber": " G1 ",
       "benefits": [{"serviceType": "maternity", "covered": True}]}


class ParseEligibilityTest(unittest.TestCase):
    def test_coverages_list_api_2026_10_01(self):
        result = verify_eligibility("aetna", "W123", {"first": "A", "last": "B", "dob": "01/02/1990", "group": None})
        self.assertTrue(result.eligible)
        self.assertEqual(result.payer_name, "Aetna")
        self.assertEqual(result.group_number, "")
        self.assertTrue(result.maternity_covered)

    def test_prefers_active_coverage(self):
        inactive = dict(COV, status="terminated", planName="Old")
        result = parse_eligibility_response({"payer": PAYER, "coverages": [inactive, COV]})
        self.assertTrue(result.eligible)
        self.assertEqual(result.plan_name, "Aetna PPO")
        self.assertEqual(result.group_number, "G1")

    def test_legacy_single_coverage(self):
        result = parse_eligibility_response({"payer": PAYER, "coverage": COV})
        self.assertTrue(result.eligible)

    def test_missing_coverage_raises_eligibility_error(self):
        for resp in ({"payer": PAYER}, {"payer": PAYER, "coverages": []}):
            with self.assertRaises(EligibilityError):
                parse_eligibility_response(resp)


if __name__ == "__main__":
    unittest.main()
