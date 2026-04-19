import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def test_recourse_output_fixture():
    obj = json.loads((ROOT / "fixtures/recourse-output.valid.json").read_text())
    assert obj["object_type"] == "RECOURSE_OUTPUT"
    assert obj["output_class"] == "recourse-object"
    assert obj["boundary_assertions"]["not-recognition"] is True
