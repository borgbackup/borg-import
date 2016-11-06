from datetime import datetime
import os


def datetime_from_mtime(path):
    """
    discover backup timestamp from a (single) filesystem object.

    e.g. from a root/TIMESTAMP file created by "touch" at backup time,
    or from root/ (assuming that the directory timestamp was modified
    at backup time).
    """
    t = os.path.getmtime(path)
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


def datetime_from_file(path):
    """
    discover backup timestamp from contents of a file.

    e.g. root/TIMESTAMP contains: Mon Oct 31 23:35:50 CET 2016
    """
    with open(path, 'r') as f:
        ts = f.readline().strip()
    return datetime_from_string(ts)

