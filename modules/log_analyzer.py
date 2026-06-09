import json
from collections import Counter

def load_logs(file_path):
    with open(file_path, "r") as file:
        return json.load(file)

def show_logs(logs):
    for log in logs:
        print(log)

def search_by_user(logs, username):
    return [log for log in logs if log["username"] == username]

def summary(logs):
    users = Counter(log["username"] for log in logs)
    statuses = Counter(log["status"] for log in logs)

    print("\nEvents per User:")
    for user, count in users.items():
        print(user, count)

    print("\nStatus Summary:")
    for status, count in statuses.items():
        print(status, count)