import os
from datetime import datetime

import pytest

from ..timestamps import datetime_from_mtime, datetime_from_string


def test_datetime_from_mtime(tmpdir):
    fn = str(tmpdir.join("mtime_test"))
    with open(fn, "w"):
        pass
    dt = datetime(1999, 12, 31, 23, 59, 59)
    atime = mtime = dt.timestamp()
    os.utime(fn, (atime, mtime))  # touch file
    assert datetime_from_mtime(fn) == dt


def test_datetime_from_string():
    assert datetime_from_string('1999-12-31T23:59:59') == \
           datetime(1999, 12, 31, 23, 59, 59)
    assert datetime_from_string('Mon Oct 31 23:35:50 CET 2016') == \
           datetime(2016, 10, 31, 23, 35, 50)
    with pytest.raises(ValueError):
        datetime_from_string('total crap')
