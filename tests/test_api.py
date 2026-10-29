import unittest

import server


class ApiTest(unittest.TestCase):
    def test_otp_verify(self):
        self.assertEqual(server.otp_verify({"code": "409549"})[0], 200)
        self.assertEqual(server.otp_verify({"code": "12"})[0], 400)

    def test_membership_lookup(self):
        status, body = server.membership_lookup({"first": "A", "last": "B", "dob": "01/02/1990", "email": "a@b.co"})
        self.assertEqual(status, 200)
        self.assertTrue(body["member_id"].startswith("PMC-"))

    def test_insurance_connect(self):
        status, body = server.insurance_connect({
            "payer": "bcbstx", "memberId": "XOJ123456789", "group": "",
            "member": {"first": "Jane", "last": "Doe", "dob": "04/12/1992"},
        })
        self.assertEqual(status, 200)
        self.assertTrue(body["eligible"])


if __name__ == "__main__":
    unittest.main()
