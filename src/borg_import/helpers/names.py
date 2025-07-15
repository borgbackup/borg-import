from datetime import datetime


def make_name(*args, dt_format="%Y-%m-%dT%H:%M:%S"):
    """
    assemble borg archive names from components.

    args can be anything that converts to str, plus:

        - bytes objects, which are safely decoded
        - datetime objects, which are formatted using dt_format

    invalid chars are replaced or removed, so the resulting archive name
    should be valid.

    E.g.:
        make_name(b'hostname', b'üser', 1)
        -> 'hostname-üser-1'

        make_name('backup name', datetime.now())
        -> 'backup_name-2016-11-01T20:28:49'
    """
    components = []
    for arg in args:
        if isinstance(arg, bytes):
            s = arg.decode("utf-8", errors="surrogateescape")
        elif isinstance(arg, datetime):
            s = arg.strftime(dt_format)
        else:
            s = str(arg)
        # we don't want to have blanks for practical shell-usage reasons:
        s = s.replace(" ", "_")
        # the slash is not allowed in archive names
        # (archive name = FUSE directory name)
        s = s.replace("/", "!")
        # :: is repo::archive separator, not allowed in archive names
        s = s.replace("::", ":")
        components.append(s)
    return "-".join(components)
