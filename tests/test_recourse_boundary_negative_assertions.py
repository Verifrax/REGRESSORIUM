import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def load(rel):
    return json.loads((ROOT / rel).read_text())

def test_forbidden_output_classes_do_not_overlap_allowed_output_classes():
    policy = load("contracts/boundary-policy.json")
    assert set(policy["allowed_output_classes"]).isdisjoint(set(policy["forbidden_output_classes"]))

def test_recourse_object_carries_non_recognition_boundary():
    obj = load("claims/current/recourse-object-0001.json")
    limits = set(obj["limits"])
    assert "recourse does not redefine law" in limits
    assert "recourse does not redefine accepted epoch" in limits
    assert "recourse does not replace authority issuance" in limits
    assert "recourse does not replace execution" in limits
    assert "recourse does not replace verification" in limits
    assert "recourse does not replace recognition" in limits

def test_current_index_shape_uses_active_truth():
    idx = load("claims/current/index.json")
    assert idx["object_type"] == "RecourseIndex"
    assert idx["status"] == "ACTIVE_TRUTH"
    assert idx["historical"] is False

def test_boundary_policy_rejection_reasons_cover_upstream_collisions():
    policy = load("contracts/boundary-policy.json")
    reasons = set(policy["rejection_reasons"])
    assert "would-author-law" in reasons
    assert "would-mutate-accepted-state" in reasons
    assert "would-issue-authority" in reasons
    assert "would-execute-governed-action" in reasons
    assert "would-emit-verification-verdict" in reasons
    assert "would-recognize-terminal-truth" in reasons
