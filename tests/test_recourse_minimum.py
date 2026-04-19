import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def load(rel: str):
    return json.loads((ROOT / rel).read_text(encoding="utf-8"))

def test_recourse_minimum():
    obj = load("claims/current/recourse-object-0001.json")
    idx = load("claims/current/index.json")

    assert obj["recourse_object_id"] == "recourse-object-0001"
    assert obj["status"] == "ACTIVE_TRUTH"
    assert obj["history_ref"] == "claims/history/"
    assert obj["authority_ref"] == "https://github.com/Verifrax/AUCTORISEAL/blob/main/authorities/current/authority-object-0001.json"
    assert obj["verification_result_ref"] == "https://github.com/Verifrax/VERIFRAX/blob/main/verification/results/current/verification-result-0001.json"
    assert obj["execution_receipt_ref"] == "https://github.com/Verifrax/CORPIFORM/blob/main/receipts/current/execution-receipt-0001.json"
    assert obj["recognition_ref"] == "https://github.com/Verifrax/ANAGNORIUM/blob/main/recognitions/current/recognition-object-0001.json"
    assert obj["continuity_transfer_boundary"] == "NON_ROLE_BOUNDARY"

    assert idx["object_type"] == "RecourseIndex"
    assert idx["status"] == "ACTIVE_TRUTH"
    assert idx["historical"] is False
    assert idx["current_recourse_object_ref"] == "claims/current/recourse-object-0001.json"

    first = idx["entries"][0]
    assert first["recourse_object_id"] == obj["recourse_object_id"]
    assert first["path"] == "claims/current/recourse-object-0001.json"
