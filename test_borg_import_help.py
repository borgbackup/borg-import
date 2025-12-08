import subprocess
import sys


def test_borg_import_help_runs():
    """Check that `borg-import --help` runs correctly."""
    result = subprocess.run(
        [sys.executable, "-m", "borg_import", "--help"],
        capture_output=True,
        text=True,
    )

    # Πρέπει να τερματίσει χωρίς error
    assert result.returncode == 0

    # Το help message πρέπει να περιέχει τη λέξη 'usage'
    combined_output = (result.stdout or "") + (result.stderr or "")
    assert "usage" in combined_output.lower()
