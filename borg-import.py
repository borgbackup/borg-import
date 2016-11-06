#!/usr/bin/env python
# temporary hack until we have a setup.py that creates the main script

import os
import sys

package_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'src'))
sys.path.insert(0, package_path)

from borg_import.main import main

if __name__ == '__main__':
    main()
