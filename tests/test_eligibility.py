import unittest

from insurance.eligibility import EligibilityError, parse_eligibility_response

PAYER = {"id": "60054", "name": "Aetna"}
COV = {"status": "active", "planName": "Aetna PPO", "groupNumber": None,
       "benefits": [{"serviceType": "maternity", "covered": True}]}


class ParseEligibilityTest(unittest.TestCase):
    def test_coverages_list(self):
        r = parse_eligibility_response({"payer": PAYER, "coverages": [COV]})
        self.assertTrue(r.eligible)
        self.assertEqual(r.plan_name, "Aetna PPO")
        self.assertEqual(r.group_number, "")
        self.assertTrue(r.maternity_covered)

    def test_prefers_active_coverage(self):
        inactive = dict(COV, status="inactive", planName="Old")
        r = parse_eligibility_response({"payer": PAYER, "coverages": [inactive, COV]})
        self.assertEqual(r.plan_name, "Aetna PPO")

    def test_legacy_coverage_object(self):
        r = parse_eligibility_response({"payer": PAYER, "coverage": dict(COV, groupNumber=" G1 ")})
        self.assertEqual(r.group_number, "G1")

    def test_empty_coverages(self):
        with self.assertRaises(EligibilityError):
            parse_eligibility_response({"payer": PAYER, "coverages": []})


if __name__ == "__main__":
    unittest.main()
