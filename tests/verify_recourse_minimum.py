#!/usr/bin/env python3
import json
import sys
from pathlib import Path

root = Path(__file__).resolve().parents[1]
errors = []

def need(cond, name):
    if cond:
        print(f"[VERIFY] {name}")
    else:
        print(f"[FAIL] {name}")
        errors.append(name)

def load(rel):
    return json.loads((root / rel).read_text(encoding="utf-8"))

obj_rel = "claims/current/recourse-object-0001.json"
idx_rel = "claims/current/index.json"
hist_rel = "claims/history/README.md"
test_rel = "tests/test_recourse_minimum.py"

need((root / obj_rel).is_file(), "recourse-object-present")
need((root / idx_rel).is_file(), "recourse-index-present")
need((root / hist_rel).is_file(), "recourse-history-present")
need((root / test_rel).is_file(), "outsider-recourse-test-present")

obj = load(obj_rel)
idx = load(idx_rel)

need(obj.get("recourse_object_id") == "recourse-object-0001", "recourse-object-id")
need(obj.get("authority_ref") == "https://github.com/Verifrax/AUCTORISEAL/blob/main/authorities/current/authority-object-0001.json", "recourse-authority-ref")
need(obj.get("verification_result_ref") == "https://github.com/Verifrax/VERIFRAX/blob/main/verification/results/current/verification-result-0001.json", "recourse-verification-ref")
need(obj.get("execution_receipt_ref") == "https://github.com/Verifrax/CORPIFORM/blob/main/receipts/current/execution-receipt-0001.json", "recourse-receipt-ref")
need(obj.get("recognition_ref") == "https://github.com/Verifrax/ANAGNORIUM/blob/main/recognitions/current/recognition-object-0001.json", "recourse-recognition-ref")
need(obj.get("continuity_transfer_boundary") == "NON_ROLE_BOUNDARY", "recourse-nonrole-continuity-transfer")

need(idx.get("object_type") == "RecourseIndex", "recourse-index-type")
need(idx.get("status") == "ACTIVE_TRUTH", "recourse-index-status")
need(idx.get("historical") is False, "recourse-index-historical-false")
need(idx.get("current_recourse_object_ref") == "claims/current/recourse-object-0001.json", "recourse-index-binding")

entries = idx.get("entries", [])
need(len(entries) >= 1, "recourse-index-entry-present")
first = entries[0] if entries else {}
need(first.get("recourse_object_id") == obj.get("recourse_object_id"), "recourse-index-entry-id")
need(first.get("path") == "claims/current/recourse-object-0001.json", "recourse-index-entry-path")

if errors:
    print("[FAIL] PHASE 4 / STEP 81 recourse minimum verification failed")
    for e in errors:
        print(f" - {e}")
    sys.exit(1)

print("[PASS] PHASE 4 / STEP 81 recourse minimum verified")
