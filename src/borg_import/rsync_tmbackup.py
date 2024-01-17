import re
from pathlib import Path

from .helpers.discover import discover, parser
from .helpers.names import make_name
from .helpers.timestamps import datetime_from_string


def get_tmbackup_snapshots(root, prefix):
    """Get all snapshot metadata discovered in the rsync root directory."""
    regex = re.compile(r'(?P<snapshot_date>.+)')

    if not Path("backup.marker").exists():
        raise FileNotFoundError("backup.marker file should exist for rsync-time-backup import")

    for path in discover(str(root), 1):
        parsed = parser(path, regex)
        if parsed is not None and parsed['snapshot_date'] not in ("latest",):
            abs_path = root / path
            meta = dict(
                name=make_name("".join([prefix, parsed['snapshot_date']])),
                path=abs_path,
                timestamp=datetime_from_string(path),
            )
            yield meta
        elif parsed['snapshot_date'] in ("latest",):
            # latest is a symlink to the most recent build. Import it anyway
            # in case user wants to do borg mount/has existing references
            # to latest.
            abs_path = root / path
            timestamp = Path("latest").resolve().name
            meta = dict(
                name=make_name("".join([prefix, "latest"])),
                path=abs_path,
                timestamp=datetime_from_string(timestamp),
            )
            yield meta
