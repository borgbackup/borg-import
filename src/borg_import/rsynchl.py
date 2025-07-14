import re

from .helpers.discover import discover, parser
from .helpers.names import make_name
from .helpers.timestamps import datetime_from_mtime


def get_rsyncsnapshots(root):
    """Get all snapshot metadata discovered in the rsync root directory."""
    regex = re.compile(r"(?P<snapshot_name>.+)")
    for path in discover(str(root), 1):
        parsed = parser(path, regex)
        if parsed is not None:
            abs_path = root / path
            meta = dict(name=make_name(parsed["snapshot_name"]), path=abs_path, timestamp=datetime_from_mtime(abs_path))
            yield meta
