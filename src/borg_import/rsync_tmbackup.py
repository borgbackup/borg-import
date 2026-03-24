import re
from pathlib import Path

from .helpers.discover import discover, parser
from .helpers.names import make_name
from .helpers.timestamps import datetime_from_string


def get_tmbackup_snapshots(root, prefix):
    """Return metadata for all snapshots discovered in the rsync root directory."""
    regex = re.compile(r"(?P<snapshot_date>.+)")

    if not (root / "backup.marker").exists():
        raise FileNotFoundError("The backup.marker file must exist for rsync-time-backup import")

    for path in discover(str(root), 1):
        parsed = parser(path, regex)
        if parsed is not None and parsed["snapshot_date"] not in ("latest",):
            abs_path = root / path
            meta = dict(
                name=make_name("".join([prefix, parsed["snapshot_date"]])),
                path=abs_path,
                timestamp=datetime_from_string(path),
            )
            yield meta
        elif parsed["snapshot_date"] in ("latest",):
            # "latest" is a symlink to the most recent backup. Import it anyway
            # in case the user wants to do borg mount or has existing references
            # to "latest".
            abs_path = root / path
            timestamp = Path("latest").resolve().name
            meta = dict(
                name=make_name("".join([prefix, "latest"])), path=abs_path, timestamp=datetime_from_string(timestamp)
            )
            yield meta
