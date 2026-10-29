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


def _select_coverage(resp):
    # Clearinghouse API 2026-10-01 returns a ``coverages`` list; older versions
    # returned a single ``coverage`` object.
    coverages = resp.get("coverages")
    if coverages is None:
        coverages = [resp["coverage"]] if resp.get("coverage") else []
    if not coverages:
        raise EligibilityError("clearinghouse returned no coverage")
    return next((c for c in coverages if c.get("status") == "active"), coverages[0])


def parse_eligibility_response(resp):
    coverage = _select_coverage(resp)
    benefits = {b["serviceType"]: b["covered"] for b in coverage.get("benefits", [])}
    return EligibilityResult(
        eligible=coverage["status"] == "active",
        payer_name=resp["payer"]["name"],
        plan_name=coverage["planName"],
        group_number=(coverage.get("groupNumber") or "").strip(),
        maternity_covered=benefits.get("maternity", False),
    )
