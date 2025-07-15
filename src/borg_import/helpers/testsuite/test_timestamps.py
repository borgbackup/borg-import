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
    dfs = datetime_from_string("1999-12-31T23:59:59")
    dt_trg = datetime(1999, 12, 31, 23, 59, 59).astimezone(tz=timezone.utc)
    assert dfs == dt_trg
    # Of course, two datetimes can be equal in different timezones. Make
    # sure the timezone info matches UTC, which borg itself expects.
    assert dfs.tzinfo == dt_trg.tzinfo == timezone.utc

    # FIXME: When this format is passed to datetime_from_string, the internal
    # strptime discards timezone info, and creates a naive time.
    # UTC is handled specially inside datetime_from_string to accommodate
    # strptime's quirks; local conversions using this format may or may not work.
    dfs = datetime_from_string("Mon Oct 31 23:35:50 UTC 2016")
    dt_trg = datetime(2016, 10, 31, 23, 35, 50, tzinfo=timezone.utc)
    assert dfs == dt_trg
    assert dfs.tzinfo == dt_trg.tzinfo == timezone.utc

    # rsync-time-backup format.
    dfs = datetime_from_string("2022-12-21-063019")
    dt_trg = datetime(2022, 12, 21, 6, 30, 19).astimezone(tz=timezone.utc)
    assert dfs == dt_trg
    assert dfs.tzinfo == dt_trg.tzinfo == timezone.utc

    with pytest.raises(ValueError):
        datetime_from_string("total crap")
