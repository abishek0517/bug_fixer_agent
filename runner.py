import subprocess

def run_code(filename):
    result = subprocess.run(
        ["python", filename],
        capture_output=True,
        text=True
    )

    return {
        "stdout": result.stdout,
        "stderr": result.stderr,
        "success": result.returncode == 0
    }