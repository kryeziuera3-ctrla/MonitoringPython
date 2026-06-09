import hashlib
import json
import os

def file_hash(path):
    sha = hashlib.sha256()

    with open(path, "rb") as f:
        while chunk := f.read(4096):
            sha.update(chunk)

    return sha.hexdigest()

def create_baseline(folder):
    baseline = {}

    for root, dirs, files in os.walk(folder):
        for file in files:
            path = os.path.join(root, file)
            baseline[path] = file_hash(path)

    with open("reports/baseline.json", "w") as f:
        json.dump(baseline, f, indent=4)

    print("Baseline created.")

def check_integrity(folder):
    with open("reports/baseline.json", "r") as f:
        baseline = json.load(f)

    changed = []

    for path, old_hash in baseline.items():
        if os.path.exists(path):
            if file_hash(path) != old_hash:
                changed.append(path)

    return changed