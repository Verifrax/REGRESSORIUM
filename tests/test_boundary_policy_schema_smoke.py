import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def test_boundary_policy_core():
    obj = json.loads((ROOT / "contracts/boundary-policy.json").read_text())
    assert obj["object_type"] == "BOUNDARY_POLICY"
    assert obj["surface"] == "REGRESSORIUM"
    assert obj["role"] == "terminal-recourse"
