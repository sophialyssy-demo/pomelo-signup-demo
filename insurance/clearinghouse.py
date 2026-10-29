"""Mock eligibility clearinghouse (stands in for a real 270/271 vendor API).

The vendor rolled out API version 2026-10-01, which returns coverage as a list
under ``coverages`` instead of a single ``coverage`` object.
"""

import uuid

API_VERSION = "2026-10-01"

PAYERS = {
    "bcbstx": {"name": "Blue Cross Blue Shield of Texas", "payer_id": "84980"},
    "aetna": {"name": "Aetna", "payer_id": "60054"},
    "uhc": {"name": "UnitedHealthcare", "payer_id": "87726"},
    "cigna": {"name": "Cigna Healthcare", "payer_id": "62308"},
    "humana": {"name": "Humana", "payer_id": "61101"},
    "medicaid_tx": {"name": "Texas Medicaid", "payer_id": "TXMCD"},
}


def check_eligibility(payer_key, member_id, first_name, last_name, dob, group_number=None):
    payer = PAYERS.get(payer_key)
    if payer is None:
        return {"apiVersion": API_VERSION, "status": "payer_not_found", "errors": [{"code": "P01"}]}
    return {
        "apiVersion": API_VERSION,
        "transactionId": str(uuid.uuid4()),
        "status": "complete",
        "payer": {"id": payer["payer_id"], "name": payer["name"]},
        "subscriber": {
            "memberId": member_id,
            "firstName": first_name.upper(),
            "lastName": last_name.upper(),
            "dateOfBirth": dob,
        },
        "coverages": [
            {
                "status": "active",
                "planName": f"{payer['name']} PPO",
                "groupNumber": group_number or None,
                "effectiveDate": "2026-01-01",
                "benefits": [{"serviceType": "maternity", "covered": True}],
            }
        ],
    }
