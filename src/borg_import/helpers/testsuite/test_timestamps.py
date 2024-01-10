import os
from datetime import datetime, timezone
from pathlib import Path

import pytest

from ..timestamps import datetime_from_mtime, datetime_from_string


def test_datetime_from_mtime(tmpdir):
    fn = Path(str(tmpdir.join("mtime_test")))
    with fn.open("w"):
        pass
    dt = datetime(1999, 12, 31, 23, 59, 59, tzinfo=timezone.utc)
    atime = mtime = dt.timestamp()
    os.utime(str(fn), (atime, mtime))  # touch file
    assert datetime_from_mtime(fn) == dt


def test_datetime_from_string():
    assert datetime_from_string('1999-12-31T23:59:59') == datetime(1999, 12, 31, 23, 59, 59)
    assert datetime_from_string('Mon Oct 31 23:35:50 UTC 2016') == datetime(2016, 10, 31, 23, 35, 50)
    with pytest.raises(ValueError):
        datetime_from_string('total crap')
