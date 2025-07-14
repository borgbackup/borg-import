import subprocess

from borg_import.main import main


def test_borg_import(tmpdir, monkeypatch):
    """Test the borg importer by creating archives in a source repo and importing them to a target repo."""
    # Create source and target repository directories
    source_repo = tmpdir.mkdir("source_repo")
    target_repo = tmpdir.mkdir("target_repo")

    # Create test data directories
    test_data = tmpdir.mkdir("test_data")
    archive1_data = test_data.mkdir("archive1")
    archive2_data = test_data.mkdir("archive2")

    # Create some test files in the archive directories
    archive1_data.join("file1.txt").write("This is file 1 in archive 1")
    archive1_data.join("file2.txt").write("This is file 2 in archive 1")
    archive2_data.join("file1.txt").write("This is file 1 in archive 2")
    archive2_data.join("file2.txt").write("This is file 2 in archive 2")

    # Initialize the source repository
    subprocess.check_call(["borg", "init", "--encryption=none", str(source_repo)])

    # Create archives in the source repository
    subprocess.check_call(["borg", "create", f"{source_repo}::archive1", "."], cwd=str(archive1_data))

    subprocess.check_call(["borg", "create", f"{source_repo}::archive2", "."], cwd=str(archive2_data))

    # Initialize the target repository
    subprocess.check_call(["borg", "init", "--encryption=none", str(target_repo)])

    # Set up command line arguments for borg-import
    monkeypatch.setattr("sys.argv", ["borg-import", "borg", str(source_repo), str(target_repo)])

    # Run the borg-import command
    main()

    # Verify that the archives were imported to the target repository
    output = subprocess.check_output(["borg", "list", "--short", str(target_repo)]).decode()
    archives = output.splitlines()

    assert "archive1" in archives
    assert "archive2" in archives

    # Extract the archives from the target repository and verify their contents
    extract_dir1 = tmpdir.mkdir("extract1")
    extract_dir2 = tmpdir.mkdir("extract2")

    subprocess.check_call(["borg", "extract", f"{target_repo}::archive1"], cwd=str(extract_dir1))

    subprocess.check_call(["borg", "extract", f"{target_repo}::archive2"], cwd=str(extract_dir2))

    # Verify the contents of the extracted archives
    assert extract_dir1.join("file1.txt").read() == "This is file 1 in archive 1"
    assert extract_dir1.join("file2.txt").read() == "This is file 2 in archive 1"
    assert extract_dir2.join("file1.txt").read() == "This is file 1 in archive 2"
    assert extract_dir2.join("file2.txt").read() == "This is file 2 in archive 2"
