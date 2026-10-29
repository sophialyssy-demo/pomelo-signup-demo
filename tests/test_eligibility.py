import unittest

from insurance import clearinghouse
from insurance.eligibility import EligibilityError, parse_eligibility_response, verify_eligibility


class EligibilityParsingTest(unittest.TestCase):
    def test_coverages_list_from_current_vendor_api(self):
        resp = clearinghouse.check_eligibility("aetna", "W123456789", "Jane", "Doe", "04/12/1992")
        self.assertIn("coverages", resp)
        result = parse_eligibility_response(resp)
        self.assertTrue(result.eligible)
        self.assertEqual(result.payer_name, "Aetna")
        self.assertEqual(result.plan_name, "Aetna PPO")
        self.assertEqual(result.group_number, "")
        self.assertTrue(result.maternity_covered)

    def test_prefers_active_coverage(self):
        resp = {
            "status": "complete",
            "payer": {"name": "Aetna"},
            "coverages": [
                {"status": "inactive", "planName": "Old", "groupNumber": "1", "benefits": []},
                {"status": "active", "planName": "New", "groupNumber": " 2 ", "benefits": []},
            ],
        }
        result = parse_eligibility_response(resp)
        self.assertTrue(result.eligible)
        self.assertEqual((result.plan_name, result.group_number), ("New", "2"))

    def test_legacy_single_coverage_object(self):
        resp = {
            "status": "complete",
            "payer": {"name": "Aetna"},
            "coverage": {"status": "active", "planName": "PPO", "groupNumber": "G1",
                         "benefits": [{"serviceType": "maternity", "covered": True}]},
        }
        self.assertTrue(parse_eligibility_response(resp).eligible)

    def test_empty_coverages_raises_eligibility_error(self):
        with self.assertRaises(EligibilityError):
            parse_eligibility_response({"status": "complete", "payer": {"name": "Aetna"}, "coverages": []})

    def test_verify_eligibility_with_group_number(self):
        result = verify_eligibility("aetna", "W123456789", {"first": "Jane", "last": "Doe", "dob": "04/12/1992", "group": " 0012 "})
        self.assertEqual(result.group_number, "0012")


if __name__ == "__main__":
    unittest.main()
