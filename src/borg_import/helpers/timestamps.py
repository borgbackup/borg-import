from datetime import datetime, timedelta
import time


def datetime_from_mtime(path):
    """
    discover backup timestamp from a (single) filesystem object.

    e.g. from a root/TIMESTAMP file created by "touch" at backup time,
    or from root/ (assuming that the directory timestamp was modified
    at backup time).
    """
    t = path.stat().st_mtime
    return datetime.fromtimestamp(t)


def datetime_from_string(s):
    """
    parse datetime from a string

    returns a datetime object if the format could be parsed.
    raises ValueError if not.
    """
    s = s.strip()
    for ts_format in [
            # ISO-8601-like:
            '%Y-%m-%dT%H:%M:%S',
            '%Y-%m-%dT%H:%M',
            '%Y-%m-%d %H:%M:%S',
            '%Y-%m-%d %H:%M',
            # date tool output [C / en_US locale]:
            '%a %b %d %H:%M:%S %Z %Y',
            # for more, see https://xkcd.com/1179/
            ]:
        try:
            return datetime.strptime(s, ts_format)
        except ValueError:
            # didn't work with this format, try next
            pass
    else:
        raise ValueError('could not parse %r' % s)


def datetime_from_dir(d, p=4):
    """
    parse datetime from part of a directory name

    returns a datetime object if the format could be parsed.
    raises ValueError if not.
    """
    if type(d).__name__ == 'PosixPath':
            s = d.name
    elif type(d) == str:
            # in case input is just a string (for testing)
            s = d
    # get rid of trailing -??? numbers that BackInTime adds
    s = s[:-p].strip()
    for ts_format in [
            # Back In Time format
            '%Y%m%d-%H%M%S',
            ]:
        try:
            dt = datetime.strptime(s, ts_format)
            # adjust time zone offset to get UTC
            tz = int(time.strftime('%z')[:-2])
            ut = dt - timedelta(hours=tz)
            return ut
        except ValueError:
            # didn't work with this format, try next
            pass
    else:
        raise ValueError('could not parse %r' % s)


def datetime_from_file(path):
    """
    discover backup timestamp from contents of a file.

    e.g. root/TIMESTAMP contains: Mon Oct 31 23:35:50 CET 2016
    """
    with path.open() as f:
        ts = f.readline().strip()
    return datetime_from_string(ts)
