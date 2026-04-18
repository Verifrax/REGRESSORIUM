import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_recourse_object_minimum():
    data = json.loads((ROOT / "claims/current/recourse-object-0001.json").read_text())
    index = json.loads((ROOT / "claims/current/index.json").read_text())

    assert data["object_type"] == "RecourseObject"
    assert data["status"] == "ACTIVE_TRUTH"
    assert data["recourse_object_id"] == "recourse-object-0001"
    assert data["recourse_index_ref"] == "claims/current/index.json"
    assert data["historical_archive_ref"] == "claims/history/"
    assert data["claim_class_ref"].endswith("/claim-classes/recourse-object.json")
    assert data["governing_law_version_ref"].endswith("/law/versions/current/law-version-0001.json")
    assert data["accepted_epoch_ref"].endswith("/epochs/current/accepted-epoch-0001.json")
    assert data["authority_object_ref"].endswith("/authorities/current/authority-object-0001.json")
    assert data["execution_receipt_ref"].endswith("/receipts/current/execution-receipt-0001.json")
    assert data["verification_result_ref"].endswith("/verification/results/current/verification-result-0001.json")
    assert data["recognition_object_ref"].endswith("/recognitions/current/recognition-object-0001.json")
    assert data["recourse_status"] == "OPEN_FOR_RECOURSE"
    assert data["closure_state"] == "OPEN"

    assert index["object_type"] == "RecourseIndex"
    assert index["status"] == "ACTIVE_TRUTH"
    assert index["current_recourse_object_ref"] == "claims/current/recourse-object-0001.json"
    assert index["entries"][0]["recourse_object_id"] == data["recourse_object_id"]
    assert index["entries"][0]["path"] == "claims/current/recourse-object-0001.json"
