import json
import os

PROCESSED_FILE = "reports/sample_logs.json"
ALERTS_FILE = "reports/alerts.json"

def monitor_new_events(log_file):

    with open(log_file, "r") as f:
        logs = json.load(f)

    if os.path.exists(PROCESSED_FILE):
        with open(PROCESSED_FILE, "r") as f:
            processed = json.load(f)
    else:
        processed = []

    new_events = []

    for event in logs:

        event_id = (
            event["timestamp"] +
            event["username"] +
            event["status"]
        )

        if event_id not in processed:

            processed.append(event_id)

            if event["status"] == "failed":

                new_events.append({
                    "event": event,
                    "severity": "HIGH"
                })

    with open(PROCESSED_FILE, "w") as f:
        json.dump(processed, f, indent=4)

    with open(ALERTS_FILE, "w") as f:
        json.dump(new_events, f, indent=4)

    return new_events
