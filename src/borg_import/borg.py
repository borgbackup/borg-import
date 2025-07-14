import subprocess

from .helpers.timestamps import datetime_from_string


def get_borg_archives(repository):
    """Get all archive metadata discovered in the Borg repository."""
    # Get list of archives with their timestamps
    borg_cmdline = ["borg", "list", "--format", "{name}{TAB}{time}{NL}", repository]
    output = subprocess.check_output(borg_cmdline).decode()

    for line in output.splitlines():
        if not line.strip():
            continue

        parts = line.split("\t", 1)
        if len(parts) == 2:
            name, timestamp_str = parts
            timestamp = datetime_from_string(timestamp_str)
            meta = dict(name=name, timestamp=timestamp, original_repository=repository)
            yield meta
