from pathlib import Path
import json

REQUIRED = [
    "README.md",
    "COUNTERPARTY.md",
    "CLAIM_CLASSES.md",
    "BURDEN_ASSIGNMENT.md",
    "REMEDY_MATRIX.md",
    "ESCALATION_FLOW.md",
    "CLOSURE_STATES.md",
    "schemas/recourse-object.schema.json",
    "claims/current/index.json",
    "closures/README.md",
    "matrices/README.md",
]

def test_recourse_surface_exists():
    for rel in REQUIRED:
        assert Path(rel).is_file(), f"missing {rel}"

def test_required_identity_sentence_present():
    text = Path("README.md").read_text(encoding="utf-8")
    assert "REGRESSORIUM is the terminal recourse plane of the Verifrax stack." in text

def test_current_index_is_current():
    obj = json.loads(Path("claims/current/index.json").read_text(encoding="utf-8"))
    assert obj["status"] == "current"
    assert obj["object_type"] == "RecourseIndex"
