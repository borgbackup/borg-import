import subprocess
from pathlib import Path


def test_rsync_tmbackup_import(tmpdir, monkeypatch):
    """Test importing rsync-time-backup style snapshots into a borg repo."""
    src = Path(str(tmpdir.mkdir("tmbackup")))

    # backup.marker is required by rsync-time-backup
    (src / "backup.marker").touch()

    # two timestamped snapshot directories
    snap1 = src / "2023-01-01-120000"
    snap1.mkdir()
    (snap1 / "file1.txt").write_text("This is file 1 in snap1")

    snap2 = src / "2023-01-02-120000"
    snap2.mkdir()
    (snap2 / "file1.txt").write_text("This is file 1 in snap2")

    target_repo = Path(str(tmpdir.mkdir("target_repo")))

    # Initialize the target repository
    subprocess.check_call(["borg", "init", "--encryption=none", str(target_repo)])

    # Run the importer
    monkeypatch.setattr(
        "sys.argv", ["borg-import", "rsync_tmbackup", "--prefix", "backup-", str(src), str(target_repo)]
    )

    from borg_import.main import main

    main()

    # Verify archives were created
    output = subprocess.check_output(["borg", "list", "--short", str(target_repo)]).decode()
    archives = output.splitlines()

    assert len(archives) == 2
    assert any("2023-01-01" in a for a in archives)
    assert any("2023-01-02" in a for a in archives)

    # Extract and verify file contents
    extract_dir = Path(str(tmpdir.mkdir("extracted")))
    first_archive = f"{target_repo}::{archives[0]}"
    subprocess.check_call(["borg", "extract", first_archive], cwd=str(extract_dir))

    restored = extract_dir / "file1.txt"
    assert restored.exists()
    assert restored.read_text() == "This is file 1 in snap1"
