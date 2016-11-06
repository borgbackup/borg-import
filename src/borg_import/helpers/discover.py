import os
import re


def discover(root, dirs_filter):
    """
    recurse starting from <root> path and yield relative dir pathes as long
    as they get through the <dirs_filter>.
    """
    for base, dirs, files in os.walk(root):
        # modify the dirs list in place, so os.walk uses it for recursion:
        dirs[:] = sorted(dirs_filter(root, base, dirs, files))
        for dir in dirs:
            abs_path = os.path.join(base, dir)
            rel_path = os.path.relpath(abs_path, root)
            yield rel_path


def depth_filter(root, base, dirs, files, max_depth):
    """filter dirs by <max_depth> (relative to root)"""
    for dir in dirs:
        abs_path = os.path.join(base, dir)
        rel_path = os.path.relpath(abs_path, root)
        depth = rel_path.count(os.path.sep) + 1
        if depth <= max_depth:
            yield dir


def parser(rel_path, regex):
    m = re.match(regex, rel_path)
    if m:
        return m.groupdict()
