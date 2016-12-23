from datetime import datetime

from ..names import make_name


def test_make_name():
    # str (some with invalid/unwanted chars)
    assert make_name('backup name') == 'backup_name'
    assert make_name('backup/name') == 'backup!name'
    assert make_name('backup::name') == 'backup:name'

    # int
    assert make_name(1, 2, 3) == '1-2-3'

    # datetime
    ts = datetime(1999, 12, 31, 23, 59, 59)
    assert make_name(ts) == '1999-12-31T23:59:59'

    # edge case
    assert make_name() == ''

    # bytes and safe decoding
    assert make_name(b'bytestring') == 'bytestring'
    s = 'äöü'
    b_utf8 = s.encode('utf-8')
    b_iso = s.encode('iso-8859-1')
    assert make_name(b_utf8) == s
    assert make_name(b_iso)  # shall not raise, surrogateescaped

    # mixed
    assert make_name(s, b_utf8, 1) == 'äöü-äöü-1'
