from datetime import datetime, timezone


def datetime_from_mtime(path):
    """
    discover backup timestamp from a (single) filesystem object.

    e.g. from a root/TIMESTAMP file created by "touch" at backup time,
    or from root/ (assuming that the directory timestamp was modified
    at backup time).
    """
    t = path.stat().st_mtime
    # Borg needs UTC timestamps.
    return datetime.fromtimestamp(t, tz=timezone.utc)


def datetime_from_string(s):
    """
    parse datetime from a string

    returns a UTC-aware datetime object if the format could be parsed.
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
            # rsync-time-backup format
            '%Y-%m-%d-%H%M%S'
            # for more, see https://xkcd.com/1179/
            ]:
        try:
            if ts_format in ('%a %b %d %H:%M:%S %Z %Y',) and 'UTC' in s:
                # %Z returns a naive datetime, despite a timezone being specified.
                # However, strptime %Z only tends to work on local times and
                # UTC.
                #
                # Per astimezone docs:
                # If self is naive, it is presumed to represent time in the
                # system timezone.
                #
                # If we had a UTC time zone, prevent conversion to aware
                # datetime from assuming a local timezone before conversion
                # to UTC.
                #
                # If "UTC" wasn't specified, assume the timezone specified
                # was local and hope for the best.
                return datetime.strptime(s, ts_format).replace(tzinfo=timezone.utc)
            else:
                return datetime.strptime(s, ts_format).astimezone(tz=timezone.utc)
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
