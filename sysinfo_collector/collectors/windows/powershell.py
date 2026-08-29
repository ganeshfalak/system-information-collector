import subprocess

def run_powershell(script):

    result = subprocess.run(
        [
            "powershell.exe",
            "-NoProfile",
            "-NonInteractive",
            "-Command",
            script,
        ],
        capture_output=True,
        text=True,
        timeout=30,
    )

    if result.returncode != 0:
        raise RuntimeError(
            f"Powershell failed ({result.returncode}): {result.stderr.strip()}"
        )

    return result.stdout.strip()