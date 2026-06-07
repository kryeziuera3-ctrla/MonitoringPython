import os

patterns = [
    "password=",
    "api_key=",
    "token=",
    "secret=",
    "private_key="
]

def scan_folder(folder):

    findings = []

    for root, dirs, files in os.walk(folder):

        for file in files:

            path = os.path.join(root, file)

            try:
                with open(path, "r", errors="ignore") as f:

                    for number, line in enumerate(f, start=1):

                        for pattern in patterns:

                            if pattern in line:
                                findings.append(
                                    f"{file} Line {number}: {pattern}"
                                )

            except:
                pass

    return findings