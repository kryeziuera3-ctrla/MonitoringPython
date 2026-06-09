from datetime import datetime

def generate_report(changes, secrets, ports, alerts):

    with open(
        "reports/final_report.txt",
        "w",
        encoding="utf-8"
    ) as report:

        report.write("SECURITY TOOLKIT REPORT\n")
        report.write(f"Generated: {datetime.now()}\n\n")

        report.write("=== FILE CHANGES ===\n")
        report.write(str(changes))
        report.write("\n\n")

        report.write("=== SECRETS FOUND ===\n")
        report.write("\n".join(secrets))
        report.write("\n\n")

        report.write("=== PORT RESULTS ===\n")
        report.write(str(ports))
        report.write("\n\n")

        report.write("=== ALERTS ===\n")
        report.write(str(alerts))