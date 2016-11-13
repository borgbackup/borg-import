import re

from ..discover import discover, parser


def test_discover(tmpdir):
    root_dir = tmpdir.mkdir('root')
    host1_dir = root_dir.mkdir('hostname1')
    host1_dir.mkdir('0')
    host1_dir.mkdir('1')
    host2_dir = root_dir.mkdir('hostname2')
    host2_dir.mkdir('3')
    dirs = list(discover(str(root_dir), 2))
    assert dirs == ['hostname1/0', 'hostname1/1', 'hostname2/3']


def test_parser():
    rx = re.compile(r'(?P<hostname>.+)/(?P<generation>.+)')
    assert parser('host1/gen0', rx) == dict(hostname='host1', generation='gen0')
    assert parser('foo', rx) is None
