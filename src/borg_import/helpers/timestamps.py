from datetime import datetime, timezone


def datetime_from_mtime(path):
    """
    Discover the backup timestamp from a (single) filesystem object.

    For example, from a root/TIMESTAMP file created by "touch" at backup time,
    or from root/ (assuming that the directory timestamp was modified
    at backup time).
    """
    t = path.stat().st_mtime
    # Borg needs timezone-aware timestamps in UTC.
    return datetime.fromtimestamp(t, tz=timezone.utc)


def datetime_from_string(s):
    """
    Parse a datetime from a string.

    Return a timezone-aware datetime object in UTC if the format could be parsed.

    Raise ValueError otherwise.
    """
    s = s.strip()
    for ts_format in [
        # ISO-8601-like:
        "%Y-%m-%dT%H:%M:%S",
        "%Y-%m-%dT%H:%M",
        "%Y-%m-%d %H:%M:%S",
        "%Y-%m-%d %H:%M",
        # date tool output [C / en_US locale]:
        "%a %b %d %H:%M:%S %Z %Y",
        # borg format with day of week
        "%a, %Y-%m-%d %H:%M:%S",
        # rsync-time-backup format
        "%Y-%m-%d-%H%M%S",
        # for more, see https://xkcd.com/1179/
    ]:
        try:
            if ts_format in ("%a %b %d %H:%M:%S %Z %Y",) and "UTC" in s:
                # %Z returns a naive datetime, despite a time zone being specified.
                # However, strptime %Z only tends to work on local times and
                # UTC.
                #
                # Per astimezone docs:
                # If self is naive, it is presumed to represent time in the
                # system time zone.
                #
                # If we had a UTC time zone, prevent conversion to an aware
                # datetime from assuming a local time zone before conversion
                # to UTC.
                return datetime.strptime(s, ts_format).replace(tzinfo=timezone.utc)
            else:
                # If "UTC" wasn't specified using the above ts_format, assume
                # the time zone specified was local and hope for the best.
                # This handles all other ts_formats as well, which are assumed
                # to be local since they don't carry a time zone.
                return datetime.strptime(s, ts_format).astimezone(tz=timezone.utc)
        except ValueError:
            # Didn't work with this format; try the next.
            pass
    else:
        raise ValueError("could not parse %r" % s)


def datetime_from_file(path):
    """
    Discover the backup timestamp from the contents of a file.

    For example, root/TIMESTAMP contains: Mon Oct 31 23:35:50 CET 2016
    """
    with path.open() as f:
        ts = f.readline().strip()
    return datetime_from_string(ts)
