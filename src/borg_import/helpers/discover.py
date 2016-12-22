import os
import re


def discover(root, depth):
    """
    recurse starting from <root> path and yield relative dir paths with wanted <depth>.
    """
    def _discover(root, current_dir, current_depth, wanted_depth):
        entries = sorted(os.listdir(current_dir))
        for entry in entries:
            path = os.path.join(current_dir, entry)
            if os.path.isdir(path):
                if current_depth == wanted_depth:
                    yield os.path.relpath(path, root)
                else:
                    for path in _discover(root, path, current_depth + 1, wanted_depth):
                        yield path

    for path in _discover(root, root, 1, depth):
        yield path


def parser(rel_path, regex):
    m = re.match(regex, rel_path)
    if m:
        return m.groupdict()
