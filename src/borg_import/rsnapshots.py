import re

from .helpers.discover import discover, parser
from .helpers.names import make_name
from .helpers.timestamps import datetime_from_mtime


def get_snapshots(root):
    """Get all snapshot metadata discovered in the rsnapshot root directory."""
    regex = re.compile(r"(?P<snapshot_id>.+)/(?P<backup_set>.+)")
    for path in discover(str(root), 2):
        parsed = parser(path, regex)
        if parsed is not None:
            abs_path = root / path
            meta = dict(
                name=make_name(parsed["backup_set"], parsed["snapshot_id"]),
                backup_set=parsed["backup_set"],
                path=abs_path,
                timestamp=datetime_from_mtime(abs_path),
            )
            yield meta
