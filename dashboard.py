from tkinter import *
from tkinter import filedialog, messagebox

from modules.log_analyzer import load_logs
from modules.file_integrity import create_baseline, check_integrity
from modules.secrets_scanner import scan_folder
from modules.port_checker import check_ports
from modules.monitoring import monitor_new_events
from modules.report_generator import generate_report

JSON_FILE = ""


def clear_output():
    output.delete("1.0", END)


def browse_json():
    global JSON_FILE

    JSON_FILE = filedialog.askopenfilename(
        filetypes=[("JSON Files", "*.json")]
    )

    if JSON_FILE:
        path_label.config(text=JSON_FILE)

        clear_output()

        output.insert(
            END,
            f"JSON Loaded Successfully\n\n{JSON_FILE}"
        )


def analyze_logs():

    if not JSON_FILE:
        messagebox.showerror(
            "Error",
            "Select JSON File First!"
        )
        return

    logs = load_logs(JSON_FILE)

    failed = 0
    success = 0

    for event in logs:

        status = str(event.get("status", "")).lower()

        if status == "failed":
            failed += 1

        elif status == "success":
            success += 1

    clear_output()

    output.insert(
        END,
        "========== LOG ANALYSIS ==========\n\n"
    )

    output.insert(
        END,
        f"Total Events      : {len(logs)}\n"
    )

    output.insert(
        END,
        f"Successful Events : {success}\n"
    )

    output.insert(
        END,
        f"Failed Events     : {failed}\n\n"
    )

    output.insert(
        END,
        "========== EVENT DETAILS ==========\n\n"
    )

    for log in logs:
        output.insert(
            END,
            str(log) + "\n"
        )


def baseline():

    create_baseline(
        "data/important_files"
    )

    clear_output()

    output.insert(
        END,
        "Baseline Created Successfully!"
    )


def integrity():

    changes = check_integrity(
        "data/important_files"
    )

    clear_output()

    output.insert(
        END,
        "========== FILE INTEGRITY ==========\n\n"
    )

    if changes:

        output.insert(
            END,
            f"Modified Files Found: {len(changes)}\n\n"
        )

        for item in changes:
            output.insert(
                END,
                str(item) + "\n"
            )

    else:

        output.insert(
            END,
            "No Changes Detected"
        )


def secrets():

    results = scan_folder(
        "data/important_files"
    )

    clear_output()

    output.insert(
        END,
        "========== SECRET SCANNER ==========\n\n"
    )

    if results:

        output.insert(
            END,
            f"Secrets Found: {len(results)}\n\n"
        )

        for item in results:
            output.insert(
                END,
                str(item) + "\n"
            )

    else:

        output.insert(
            END,
            "No Secrets Found"
        )


def ports():

    results = check_ports(
        [21, 22, 80, 443, 3306]
    )

    clear_output()

    output.insert(
        END,
        "========== PORT SCAN ==========\n\n"
    )

    open_ports = 0

    for port, status in results.items():

        output.insert(
            END,
            f"Port {port}: {status}\n"
        )

        if status == "OPEN":
            open_ports += 1

    output.insert(
        END,
        f"\nTotal Open Ports: {open_ports}"
    )


def monitoring():

    if not JSON_FILE:
        messagebox.showerror(
            "Error",
            "Select JSON File First!"
        )
        return

    alerts = monitor_new_events(
        JSON_FILE
    )

    clear_output()

    output.insert(
        END,
        "========== SECURITY ALERTS ==========\n\n"
    )

    if alerts:

        output.insert(
            END,
            f"Total Alerts: {len(alerts)}\n\n"
        )

        for alert in alerts:

            output.insert(
                END,
                str(alert) + "\n\n"
            )

    else:

        output.insert(
            END,
            "No Alerts Found"
        )


def report():

    changes = check_integrity(
        "data/important_files"
    )

    secrets_found = scan_folder(
        "data/important_files"
    )

    ports_found = check_ports(
        [21, 22, 80, 443, 3306]
    )

    alerts = []

    if JSON_FILE:

        try:
            alerts = monitor_new_events(
                JSON_FILE
            )
        except:
            pass

    generate_report(
        changes,
        secrets_found,
        ports_found,
        alerts
    )

    open_ports = sum(
        1 for status in ports_found.values()
        if status == "OPEN"
    )

    clear_output()

    report_text = f"""
============================================================
            ALBACOM CYBER SECURITY REPORT
============================================================

GENERAL SUMMARY

Modified Files : {len(changes)}
Secrets Found  : {len(secrets_found)}
Open Ports     : {open_ports}
Security Alerts: {len(alerts)}

============================================================

FILE INTEGRITY RESULTS

{changes}

============================================================

SECRET SCANNER RESULTS

{secrets_found}

============================================================

PORT RESULTS

{ports_found}

============================================================

MONITORING ALERTS

{alerts}

============================================================

REPORT SAVED:

reports/final_report.txt

STATUS: SUCCESSFULLY GENERATED

============================================================
"""

    output.insert(
        END,
        report_text
    )


root = Tk()

root.title(
    "ALBACOM Cyber Security Monitoring System"
)

root.geometry(
    "1300x800"
)

root.configure(
    bg="#111111"
)

title = Label(
    root,
    text="ALBACOM CYBER SECURITY MONITORING SYSTEM",
    bg="#111111",
    fg="white",
    font=("Arial", 24, "bold")
)

title.pack(
    pady=15
)

btn_frame = Frame(
    root,
    bg="#111111"
)

btn_frame.pack(
    pady=10
)

buttons = [
    ("Browse JSON", browse_json),
    ("Analyze Logs", analyze_logs),
    ("Create Baseline", baseline),
    ("Integrity Check", integrity),
    ("Secret Scanner", secrets),
    ("Port Checker", ports),
    ("Monitoring", monitoring),
    ("Generate Report", report)
]

row = 0
col = 0

for text, command in buttons:

    Button(
        btn_frame,
        text=text,
        command=command,
        width=22,
        height=2,
        bg="#222222",
        fg="white"
    ).grid(
        row=row,
        column=col,
        padx=6,
        pady=6
    )

    col += 1

    if col == 4:
        col = 0
        row += 1

path_label = Label(
    root,
    text="No JSON File Selected",
    bg="#111111",
    fg="lightgreen",
    font=("Arial", 10)
)

path_label.pack(
    pady=10
)

output = Text(
    root,
    bg="black",
    fg="white",
    font=("Consolas", 11)
)

output.pack(
    fill=BOTH,
    expand=True,
    padx=20,
    pady=20
)

output.insert(
    END,
    """
============================================================
ALBACOM CYBER SECURITY MONITORING SYSTEM
============================================================

WELCOME

• Browse JSON
• Analyze Logs
• Create Baseline
• Integrity Check
• Secret Scanner
• Port Checker
• Monitoring
• Generate Report

Select a JSON file and start analysis.
"""
)

root.mainloop()