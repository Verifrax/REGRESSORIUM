#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def load(rel):
    p = ROOT / rel
    if not p.exists():
        raise SystemExit(f"FAIL missing-file {rel}")
    try:
        return json.loads(p.read_text())
    except Exception as e:
        raise SystemExit(f"FAIL invalid-json {rel}: {e}")

def need(cond, msg):
    if not cond:
        raise SystemExit(f"FAIL {msg}")

policy = load("contracts/boundary-policy.json")
recourse_schema = load("schemas/recourse-object.schema.json")
output_schema = load("schemas/recourse-output.schema.json")
audit_schema = load("schemas/recourse-audit-record.schema.json")
current_obj = load("claims/current/recourse-object-0001.json")
current_idx = load("claims/current/index.json")
output_fixture = load("fixtures/recourse-output.valid.json")
audit_fixture = load("fixtures/recourse-audit-record.valid.json")

print("[VERIFY] files-present")

need(policy["object_type"] == "BOUNDARY_POLICY", "boundary policy object_type")
need(policy["surface"] == "REGRESSORIUM", "boundary policy surface")
need(policy["role"] == "terminal-recourse", "boundary policy role")

allowed = set(policy["allowed_output_classes"])
forbidden = set(policy["forbidden_output_classes"])
need(allowed.isdisjoint(forbidden), "allowed/forbidden overlap")

required_reasons = {
    "would-author-law",
    "would-mutate-accepted-state",
    "would-issue-authority",
    "would-execute-governed-action",
    "would-emit-verification-verdict",
    "would-recognize-terminal-truth"
}
need(required_reasons.issubset(set(policy["rejection_reasons"])), "missing rejection reasons")

print("[VERIFY] boundary-policy-core")

need(current_obj["object_type"] == "RecourseObject", "current recourse object type")
need(current_obj["status"] == "ACTIVE_TRUTH", "current recourse object status")
need(current_obj["recourse_index_ref"] == "claims/current/index.json", "recourse index ref")
need(current_obj["historical_archive_ref"] == "claims/history/", "historical archive ref")
need(current_obj["recognition_object_ref"].endswith("/recognitions/current/recognition-object-0001.json"), "recognition object ref")
need(current_obj["recourse_status"] == "OPEN_FOR_RECOURSE", "recourse status")
need(current_obj["closure_state"] == "OPEN", "closure state")

limits = set(current_obj["limits"])
need("recourse does not redefine law" in limits, "missing non-law limit")
need("recourse does not replace verification" in limits, "missing non-verification limit")
need("recourse does not replace recognition" in limits, "missing non-recognition limit")

print("[VERIFY] recourse-object-core")

need(current_idx["object_type"] == "RecourseIndex", "current index type")
need(current_idx["status"] == "ACTIVE_TRUTH", "current index status")
need(current_idx["historical"] is False, "current index historical false")
need(current_idx["current_recourse_object_ref"] == "claims/current/recourse-object-0001.json", "current object ref")
need(current_idx["entries"][0]["path"] == "claims/current/recourse-object-0001.json", "index entry path")

print("[VERIFY] recourse-index-core")

need(output_fixture["object_type"] == "RECOURSE_OUTPUT", "output fixture type")
need(output_fixture["boundary_assertions"]["not-recognition"] is True, "output fixture non-recognition")
need(audit_fixture["object_type"] == "RECOURSE_AUDIT_RECORD", "audit fixture type")
need(audit_fixture["decision"] == "rejected", "audit fixture decision")
need(audit_fixture["rejection_reason"] == "would-recognize-terminal-truth", "audit fixture reason")
need(audit_fixture["sovereign_collision_flags"]["recognition"] is True, "audit fixture recognition flag")

print("[VERIFY] output-and-audit-core")

try:
    import jsonschema  # type: ignore
except Exception:
    print("[VERIFY] jsonschema-module absent -> structural verification only")
else:
    from jsonschema import Draft202012Validator, FormatChecker  # type: ignore
    Draft202012Validator(recourse_schema, format_checker=FormatChecker()).validate(current_obj)
    Draft202012Validator(output_schema, format_checker=FormatChecker()).validate(output_fixture)
    Draft202012Validator(audit_schema, format_checker=FormatChecker()).validate(audit_fixture)
    Draft202012Validator(load("schemas/boundary-policy.schema.json"), format_checker=FormatChecker()).validate(policy)
    print("[VERIFY] full-jsonschema-validation")

print("[PASS] PHASE 2 / STEP 12 boundary-object minimum verified")
