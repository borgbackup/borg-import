import subprocess
import sys
import shlex


def test_borg_import_help_runs():
    """Check that `python -m borg_import --help` executes successfully."""
    cmd = f"{sys.executable} -m borg_import --help"
    result = subprocess.run(
        shlex.split(cmd),
        capture_output=True,
        text=True,
    )

    assert result.returncode == 0
    assert "usage" in (result.stdout + result.stderr).lower()
