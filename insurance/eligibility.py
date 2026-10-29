"""Insurance eligibility verification used by the signup flow."""

from dataclasses import dataclass

from . import clearinghouse


class EligibilityError(Exception):
    pass


@dataclass
class EligibilityResult:
    eligible: bool
    payer_name: str
    plan_name: str
    group_number: str
    maternity_covered: bool


def verify_eligibility(payer_key, member_id, member):
    resp = clearinghouse.check_eligibility(
        payer_key,
        member_id,
        member.get("first", ""),
        member.get("last", ""),
        member.get("dob", ""),
        member.get("group"),
    )
    if resp.get("status") != "complete":
        raise EligibilityError(f"clearinghouse status={resp.get('status')}")
    return parse_eligibility_response(resp)


def parse_eligibility_response(resp):
    coverage = resp["coverage"]
    benefits = {b["serviceType"]: b["covered"] for b in coverage["benefits"]}
    return EligibilityResult(
        eligible=coverage["status"] == "active",
        payer_name=resp["payer"]["name"],
        plan_name=coverage["planName"],
        group_number=coverage["groupNumber"].strip(),
        maternity_covered=benefits.get("maternity", False),
    )
